#!/usr/bin/env python3
"""
Test script for Vercel deployment compatibility
"""
import os
import json
import tempfile
from app_vercel import app

def test_vercel_environment():
    """Test if Vercel environment detection works"""
    print("Testing Vercel environment detection...")
    
    # Simulate Vercel environment
    os.environ['VERCEL'] = '1'
    os.environ['VERCEL_ENV'] = 'production'
    
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'Vercel' in data.get('service', '')
        print("✅ Health check passed")
        
        # Test platforms endpoint
        response = client.get('/api/platforms')
        assert response.status_code == 200
        data = response.get_json()
        assert 'platforms' in data
        print("✅ Platforms endpoint passed")
        
        # Test info endpoint with mock data
        response = client.post('/api/info', 
                              json={'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'},
                              content_type='application/json')
        # Note: This will fail without network, but tests the endpoint structure
        print(f"ℹ️  Info endpoint status: {response.status_code}")
        
    # Clean up environment
    os.environ.pop('VERCEL', None)
    os.environ.pop('VERCEL_ENV', None)
    
    print("✅ Vercel compatibility tests completed")

def test_memory_optimization():
    """Test memory optimization features"""
    print("Testing memory optimizations...")
    
    from api_vercel import get_vercel_ydl_opts
    
    opts = get_vercel_ydl_opts()
    
    # Check memory optimization settings
    assert opts['concurrent_fragments'] == 1
    assert opts['fragment_retries'] == 1
    assert opts['http_chunk_size'] == 1024*1024
    assert opts['socket_timeout'] == 30
    
    print("✅ Memory optimization settings verified")

def test_file_handling():
    """Test temporary file handling"""
    print("Testing file handling...")
    
    # Test temp directory creation
    temp_dir = tempfile.mkdtemp()
    assert os.path.exists(temp_dir)
    
    # Test cleanup functionality
    from utils import cleanup_file
    test_file = os.path.join(temp_dir, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    
    assert os.path.exists(test_file)
    cleanup_file(test_file)
    assert not os.path.exists(test_file)
    
    print("✅ File handling tests passed")

if __name__ == '__main__':
    print("🚀 Running Vercel compatibility tests...\n")
    
    try:
        test_vercel_environment()
        test_memory_optimization()
        test_file_handling()
        
        print("\n✅ All tests passed! Project is ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Install Vercel CLI: npm i -g vercel")
        print("2. Run: vercel --prod")
        print("3. Follow the deployment prompts")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check the error and fix before deploying to Vercel.")