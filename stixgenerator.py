import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class STIXGenerator:
    """
    STIX Generator class
    """
    def __init__(self):
        self.sco_types = [
            'artifact', 'autonomous-system', 'directory', 'domain-name', 'email-addr', 
            'email-message', 'file', 'ipv4-addr', 'ipv6-addr', 'mac-addr', 'mutex', 
            'network-traffic', 'process', 'software', 'url', 'user-account', 
            'windows-registry-key', 'x509-certificate', 'crypto-currency-wallet', 
            'crypto-currency-transaction'
        ]
        
        self.sdo_types = [
            'attack-pattern', 'campaign', 'course-of-action', 'grouping', 'identity', 
            'indicator', 'infrastructure', 'intrusion-set', 'location', 'malware', 
            'malware-analysis', 'note', 'observed-data', 'opinion', 'report', 
            'threat-actor', 'tool', 'vulnerability'
        ]
        
        self.relationship_constraints = {
            "version": "2.1",
            "relationships": {
                "indicator": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "malware", "tool", "threat-actor", "infrastructure", "vulnerability"],
                    "relationship_types": ["indicates", "related-to"]
                },
                "malware": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "tool", "threat-actor", "infrastructure", "vulnerability"],
                    "relationship_types": ["uses", "targets", "related-to", "downloads", "drops"]
                },
                "observed-data": {
                    "allowed_targets": ["indicator", "malware", "tool", "threat-actor", "attack-pattern", "campaign", "intrusion-set"],
                    "relationship_types": ["related-to"]
                },
                "threat-actor": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "malware", "tool", "infrastructure", "vulnerability", "identity", "location"],
                    "relationship_types": ["uses", "targets", "attributed-to", "related-to", "impersonates", "located-at"]
                },
                "attack-pattern": {
                    "allowed_targets": ["campaign", "intrusion-set", "indicator", "malware", "tool", "threat-actor", "vulnerability", "course-of-action"],
                    "relationship_types": ["uses", "targets", "related-to", "mitigated-by"]
                },
                "campaign": {
                    "allowed_targets": ["attack-pattern", "intrusion-set", "indicator", "malware", "tool", "threat-actor", "infrastructure", "vulnerability", "identity"],
                    "relationship_types": ["uses", "targets", "attributed-to", "related-to"]
                },
                "intrusion-set": {
                    "allowed_targets": ["attack-pattern", "campaign", "indicator", "malware", "tool", "threat-actor", "infrastructure", "vulnerability", "identity"],
                    "relationship_types": ["uses", "targets", "attributed-to", "related-to"]
                },
                "tool": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "malware", "threat-actor", "infrastructure", "vulnerability"],
                    "relationship_types": ["uses", "targets", "related-to", "drops"]
                },
                "infrastructure": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "malware", "tool", "threat-actor", "vulnerability"],
                    "relationship_types": ["uses", "hosts", "related-to", "communicates-with"]
                },
                "vulnerability": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "malware", "tool", "threat-actor", "course-of-action"],
                    "relationship_types": ["related-to", "mitigated-by"]
                },
                "course-of-action": {
                    "allowed_targets": ["attack-pattern", "vulnerability", "malware", "tool"],
                    "relationship_types": ["mitigates", "related-to"]
                },
                "identity": {
                    "allowed_targets": ["attack-pattern", "campaign", "intrusion-set", "indicator", "malware", "tool", "threat-actor", "infrastructure", "vulnerability"],
                    "relationship_types": ["related-to", "targets"]
                },
                "location": {
                    "allowed_targets": ["identity", "threat-actor", "campaign", "intrusion-set"],
                    "relationship_types": ["related-to", "located-at"]
                }
            }
        }
    
    def generate_id(self, object_type: str) -> str:
        return f"{object_type}--{str(uuid.uuid4())}"
    
    def get_current_timestamp(self) -> str:
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    def create_stix_object(self, object_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a STIX object
        """
        stix_object = {
            "type": object_type,
            "id": self.generate_id(object_type),
            "spec_version": "2.1",
            "created": self.get_current_timestamp(),
            "modified": self.get_current_timestamp()
        }
        stix_object.update(properties)
        
        return stix_object
    
    def create_relationship(self, source_ref: str, target_ref: str, relationship_type: str) -> Dict[str, Any]:
        """
        Create a STIX relationship object
        """
        return self.create_stix_object("relationship", {
            "source_ref": source_ref,
            "target_ref": target_ref,
            "relationship_type": relationship_type
        })
    
    def validate_relationship(self, source_type: str, target_type: str, relationship_type: str) -> bool:
        """
        Validate if a relationship is allowed between two object types
        """
        # If no constraints defined for source type, allow all relationships
        constraints = self.relationship_constraints.get("relationships", {})
        source_constraints = constraints.get(source_type, {})

        if not source_constraints:
            return True
        
        allowed_targets = source_constraints.get("allowed_targets", [])
        allowed_relationship_types = source_constraints.get("relationship_types", [])
        target_allowed = not allowed_targets or target_type in allowed_targets
        relationship_allowed = not allowed_relationship_types or relationship_type in allowed_relationship_types
        
        return target_allowed and relationship_allowed
    
    def create_bundle(self, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a STIX bundle containing multiple objects
        """
        return {
            "type": "bundle",
            "id": self.generate_id("bundle"),
            "objects": objects
        }
    
    def validate_bundle(self, bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a STIX bundle structure
        """
        errors = []
        warnings = []
        
        if bundle.get("type") != "bundle":
            errors.append("Bundle must have type 'bundle'")
        
        if "objects" not in bundle or not isinstance(bundle["objects"], list):
            errors.append("Bundle must contain an 'objects' array")
        
        if "objects" in bundle:
            for obj in bundle["objects"]:
                if obj.get("type") in self.sco_types:
                    errors.append(f"SCO '{obj.get('type')}' cannot be a top-level object")

        observed_data_objects = [obj for obj in bundle.get("objects", []) if obj.get("type") == "observed-data"]
        
        for obj in observed_data_objects:
            if not obj.get("number_observed") or obj.get("number_observed") < 1:
                errors.append(f"observed-data {obj.get('id')} must have number_observed >= 1")
            
            if not obj.get("first_observed") or not obj.get("last_observed"):
                errors.append(f"observed-data {obj.get('id')} must have first_observed and last_observed")
            
            # Checking for nested SCOs
            if "objects" in obj:
                for sco_key, sco in obj["objects"].items():
                    if sco.get("id") or sco.get("spec_version"):
                        errors.append(f"SCO in observed-data.objects must not include id or spec_version")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def create_indicator(self, pattern: str, labels: List[str], **kwargs) -> Dict[str, Any]:
        """
        Create a STIX Indicator object
        """
        properties = {
            "pattern": pattern,
            "labels": labels,
            "valid_from": self.get_current_timestamp()
        }
        properties.update(kwargs)
        return self.create_stix_object("indicator", properties)
    
    def create_malware(self, name: str, labels: List[str], **kwargs) -> Dict[str, Any]:
        """
        Create a STIX Malware object
        """
        properties = {
            "name": name,
            "labels": labels
        }
        properties.update(kwargs)
        return self.create_stix_object("malware", properties)
    
    def create_threat_actor(self, name: str, labels: List[str], **kwargs) -> Dict[str, Any]:
        """
        Create a STIX Threat Actor object
        """
        properties = {
            "name": name,
            "labels": labels
        }
        properties.update(kwargs)
        return self.create_stix_object("threat-actor", properties)
    
    def create_observed_data(self, number_observed: int, first_observed: str, last_observed: str, objects: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a STIX Observed Data object
        """
        properties = {
            "number_observed": number_observed,
            "first_observed": first_observed,
            "last_observed": last_observed,
            "objects": objects
        }
        return self.create_stix_object("observed-data", properties)
    
    def export_bundle_to_file(self, bundle: Dict[str, Any], filename: str) -> None:
        """
        Export a STIX bundle to a JSON file
        """
        with open(filename, 'w') as f:
            json.dump(bundle, f, indent=2)
    
    def import_bundle_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Import a STIX bundle from a JSON file
        """
        with open(filename, 'r') as f:
            return json.load(f)