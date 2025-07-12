from bottle import Bottle, run, static_file, request, response
import json
import os
from stixgenerator import STIXGenerator

stix_generator = STIXGenerator()

app = Bottle()

session_objects = []
session_relationships = []

@app.route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')

@app.route('/')
def index():
    return static_file('index.html', root='.')

@app.route('/api/validate-bundle', method='POST')
def validate_bundle():
    try:
        bundle_data = request.json
        if not bundle_data:
            response.status = 400
            return {'error': 'No bundle data provided'}
        
        validation_result = stix_generator.validate_bundle(bundle_data)
        return validation_result
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Endpoint to create STIX objects
@app.route('/api/create-object', method='POST')
def create_object():
    try:
        data = request.json
        object_type = data.get('type')
        properties = data.get('properties', {})
        
        if not object_type:
            response.status = 400
            return {'error': 'Object type is required'}

        if object_type == 'indicator':
            if 'pattern' not in properties or 'labels' not in properties:
                response.status = 400
                return {'error': 'Indicator requires pattern and labels'}
            stix_object = stix_generator.create_indicator(
                properties['pattern'], 
                properties['labels'], 
                **{k: v for k, v in properties.items() if k not in ['pattern', 'labels']}
            )
        elif object_type == 'malware':
            if 'name' not in properties or 'labels' not in properties:
                response.status = 400
                return {'error': 'Malware requires name and labels'}
            stix_object = stix_generator.create_malware(
                properties['name'], 
                properties['labels'], 
                **{k: v for k, v in properties.items() if k not in ['name', 'labels']}
            )
        elif object_type == 'threat-actor':
            if 'name' not in properties or 'labels' not in properties:
                response.status = 400
                return {'error': 'Threat Actor requires name and labels'}
            stix_object = stix_generator.create_threat_actor(
                properties['name'], 
                properties['labels'], 
                **{k: v for k, v in properties.items() if k not in ['name', 'labels']}
            )
        elif object_type == 'observed-data':
            required_fields = ['number_observed', 'first_observed', 'last_observed', 'objects']
            if not all(field in properties for field in required_fields):
                response.status = 400
                return {'error': f'Observed Data requires: {", ".join(required_fields)}'}
            stix_object = stix_generator.create_observed_data(
                properties['number_observed'],
                properties['first_observed'],
                properties['last_observed'],
                properties['objects']
            )
        else:
            stix_object = stix_generator.create_stix_object(object_type, properties)

        session_objects.append(stix_object)
        
        return stix_object
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Endpoint to create relationships 
@app.route('/api/create-relationship', method='POST')
def create_relationship():
    try:
        data = request.json
        source_ref = data.get('source_ref')
        target_ref = data.get('target_ref')
        relationship_type = data.get('relationship_type')
        
        if not all([source_ref, target_ref, relationship_type]):
            response.status = 400
            return {'error': 'source_ref, target_ref, and relationship_type are required'}

        source_type = source_ref.split('--')[0]
        target_type = target_ref.split('--')[0]
        
        if not stix_generator.validate_relationship(source_type, target_type, relationship_type):
            response.status = 400
            return {'error': f'Invalid relationship: {source_type} -{relationship_type}-> {target_type}'}
        
        relationship = stix_generator.create_relationship(source_ref, target_ref, relationship_type)
        session_relationships.append(relationship)
        
        return relationship
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Endpoint to create bundles
@app.route('/api/create-bundle', method='POST')
def create_bundle():
    try:
        data = request.json
        objects = data.get('objects', [])
        include_session_data = data.get('include_session_data', True)
        all_objects = objects.copy()
        
        if include_session_data:
            all_objects.extend(session_objects)
            all_objects.extend(session_relationships)
        
        if not all_objects:
            response.status = 400
            return {'error': 'No objects to include in bundle'}
        
        bundle = stix_generator.create_bundle(all_objects)
        validation_result = stix_generator.validate_bundle(bundle)
        
        return {
            'bundle': bundle,
            'validation': validation_result,
            'total_objects': len(all_objects),
            'session_objects': len(session_objects),
            'session_relationships': len(session_relationships)
        }
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# New endpoint to get current session data
@app.route('/api/session-data', method='GET')
def get_session_data():
    return {
        'objects': session_objects,
        'relationships': session_relationships,
        'total_objects': len(session_objects),
        'total_relationships': len(session_relationships)
    }

# New endpoint to clear session data
@app.route('/api/clear-session', method='POST')
def clear_session():
    global session_objects, session_relationships
    session_objects = []
    session_relationships = []
    return {'message': 'Session data cleared'}

# Endpoint to save the STIX bundle
@app.route('/api/save-bundle', method='POST')
def save_bundle():
    try:
        bundle_data = request.json
        if not bundle_data or bundle_data.get('type') != 'bundle':
            response.status = 400
            return {'error': 'Invalid STIX bundle format'}
        
        validation_result = stix_generator.validate_bundle(bundle_data)
        if not validation_result['valid']:
            response.status = 400
            return {
                'error': 'Bundle validation failed',
                'validation_errors': validation_result['errors']
            }
        
        # Ensure bundles directory exists
        if not os.path.exists('bundles'):
            os.makedirs('bundles')
        
        filename = f"stix_bundle_{bundle_data.get('id', 'unknown').replace('bundle--', '')}.json"
        bundle_path = os.path.join('bundles', filename)
        
        stix_generator.export_bundle_to_file(bundle_data, bundle_path)
        
        return {
            'success': True, 
            'filename': filename,
            'validation': validation_result
        }
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Endpoint to load the STIX bundle
@app.route('/api/bundles')
def list_bundles():
    try:
        bundles_dir = 'bundles'
        if not os.path.exists(bundles_dir):
            os.makedirs(bundles_dir)
            return {'bundles': []}
        
        bundle_files = [f for f in os.listdir(bundles_dir) if f.endswith('.json')]
        bundles = []
        
        for filename in bundle_files:
            try:
                bundle_path = os.path.join(bundles_dir, filename)
                bundle = stix_generator.import_bundle_from_file(bundle_path)
                validation_result = stix_generator.validate_bundle(bundle)
                
                bundles.append({
                    'filename': filename,
                    'id': bundle.get('id'),
                    'objects_count': len(bundle.get('objects', [])),
                    'created': os.path.getctime(bundle_path),
                    'valid': validation_result['valid'],
                    'validation_errors': validation_result.get('errors', [])
                })
            except Exception as e:
                bundles.append({
                    'filename': filename,
                    'error': f'Failed to load: {str(e)}',
                    'valid': False
                })
                continue
        
        return {'bundles': bundles}
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# API endpoint to load a specific bundle
@app.route('/api/bundle/<filename>')
def get_bundle(filename):
    try:
        bundle_path = os.path.join('bundles', filename)
        if not os.path.exists(bundle_path):
            response.status = 404
            return {'error': 'Bundle not found'}
        
        bundle = stix_generator.import_bundle_from_file(bundle_path)
        validation_result = stix_generator.validate_bundle(bundle)
        
        return {
            'bundle': bundle,
            'validation': validation_result
        }
    
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Get available STIX object types
@app.route('/api/object-types')
def get_object_types():
    return {
        'sdo_types': stix_generator.sdo_types,
        'sco_types': stix_generator.sco_types,
        'relationship_constraints': stix_generator.relationship_constraints
    }

# Enable CORS
@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/<path:path>', method='OPTIONS')
def handle_options(path):
    return {}

if __name__ == '__main__':
    if not os.path.exists('bundles'):
        os.makedirs('bundles')
    # Debug is true for dev purposes
    run(app, host='localhost', port=8080, debug=True, reloader=True)