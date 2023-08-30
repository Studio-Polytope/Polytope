import pytest

import polytope.utils.uuidgen as uuidgen


def test_uuid_collision():
    # fail probability ~ 5 * 10^-5
    uuids = [uuidgen.uuid() for _ in range(10000)]
    assert len(uuids) == len(set(uuids))

def test_default():
    gen = uuidgen.PolytopeUUID()
    assert len(gen.alphabet) == 32
    assert gen.length == 8

def test_gen_uuid():
    gen = uuidgen.PolytopeUUID(alphabet='0123456789', length=15)
    assert gen.alphabet == '0123456789'
    assert gen.length == 15

    gen.length = 15
    uuid = gen.uuid()
    assert len(uuid) == 15
    for c in uuid:
        assert c in gen.alphabet

    gen = uuidgen.PolytopeUUID(length=300)
    assert len(gen.alphabet) == 32
    assert gen.length == 300

    for _ in range(300):
        uuid = gen.uuid()
        assert len(uuid) == 300
        for c in uuid:
            assert c in gen.alphabet

def test_gen_bulk():
    gen = uuidgen.PolytopeUUID(length=300)

    uuids = gen.uuid_bulk(3000)
    assert len(uuids) == 3000
    assert len(uuids) == len(set(uuids))

    for uuid in uuids:
        assert len(uuid) == 300
        for c in uuid:
            assert c in gen.alphabet

def test_uuid():
    alphabet = '0123456789'
    uuid = uuidgen.uuid(alphabet, 12)
    assert len(uuid) == 12
    for c in uuid:
        assert c in alphabet

    for _ in range(300):
        uuid = uuidgen.uuid(alphabet, 300)
        assert len(uuid) == 300
        for c in uuid:
            assert c in alphabet

def test_bulk():
    alphabet = '0123456789'

    uuids = uuidgen.uuid_bulk(count=3000, alphabet=alphabet, length=300)
    assert len(uuids) == 3000
    assert len(uuids) == len(set(uuids))

    for uuid in uuids:
        assert len(uuid) == 300
        for c in uuid:
            assert c in alphabet

def test_value_error():
    # Too few alphabets
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet="")
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet="abc")
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet="012345678")

    # Duplicated alphabets
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet='aaabbbcccdddeee')
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet='bcdAefghijklmAno')

    # Too small length
    with pytest.raises(ValueError):
        uuid = uuidgen.uuid('0123456789', -1)
    with pytest.raises(ValueError):
        uuid = uuidgen.uuid('0123456789', 0)
    with pytest.raises(ValueError):
        uuid = uuidgen.uuid('0123456789', 4)

    # Too large count
    with pytest.raises(ValueError):
        uuids = uuidgen.uuid_bulk(1100, '0123456789', 5)
