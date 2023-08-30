import pytest

import polytope.utils.uuidgen as uuidgen


def test_uuid_collision():
    # fail probability ~ 5 * 10^-5
    uuids = [uuidgen.uuid() for _ in range(10000)]
    assert len(uuids) == len(set(uuids))

def test_uuid():
    assert len(uuidgen.uuid('abcde', 3)) == 3

    gen = uuidgen.PolytopeUUID(alphabet='abcde', length=15)
    assert gen.alphabet == 'abcde'
    assert gen.length == 15

    gen.length = 5
    uuid = gen.uuid()
    assert len(uuid) == 5
    for c in uuid:
        assert c in gen.alphabet

    gen = uuidgen.PolytopeUUID()
    assert len(gen.alphabet) == 32
    assert gen.length == 8

def test_large_uuid():
    gen = uuidgen.PolytopeUUID(length=300)
    assert len(gen.alphabet) == 32
    assert gen.length == 300

    for _ in range(300):
        uuid = gen.uuid()
        assert len(uuid) == 300
        for c in uuid:
            assert c in gen.alphabet

def test_bulk():
    uuids = uuidgen.uuid_bulk(9, 'abc', 2)
    for uuid in uuids:
        assert len(uuid) == 2
        for c in uuid:
            assert c in 'abc'
    assert(len(uuids) == len(set(uuids)))

    gen = uuidgen.PolytopeUUID('abc', 2)
    uuids = gen._PolytopeUUID__uuid_bulk_large(4)
    for uuid in uuids:
        assert len(uuid) == 2
        for c in uuid:
            assert c in 'abc'
    assert(len(uuids) == len(set(uuids)))

def test_large_bulk():
    gen = uuidgen.PolytopeUUID(length=300)

    uuids = gen.uuid_bulk(3000)
    assert len(uuids) == 3000
    assert len(uuids) == len(set(uuids))

    for uuid in uuids:
        assert len(uuid) == 300
        for c in uuid:
            assert c in gen.alphabet

def test_value_error():
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet='aa')

    with pytest.raises(ValueError):
        uuid = uuidgen.uuid('abcd', 0)

    with pytest.raises(ValueError):
        uuids = uuidgen.uuid_bulk(10, 'abc', 2)

    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet='abc', length=2)
        uuids = gen._PolytopeUUID__uuid_bulk_large(5)
