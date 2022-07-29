from networks import __version__, batcher_sort, certify_network


def test_version():
    assert __version__ == '0.1.0'

def test_network():
    network = list(batcher_sort(512))
    status, proof = certify_network(network, with_proof = True, solver_name = 'glucose3')

    assert status
    
    
