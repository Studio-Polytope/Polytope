import pytest

import polytope.core.uuidgen as uuidgen


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

def test_bulk():
    uuids = uuidgen.uuid_bulk(9, 'abc', 2)
    for uuid in uuids:
        assert len(uuid) == 2
        for c in uuid:
            assert c in 'abc'
    assert(len(uuids) == len(set(uuids)))

def test_value_error():
    with pytest.raises(ValueError):
        gen = uuidgen.PolytopeUUID(alphabet='aa')

    with pytest.raises(ValueError):
        uuid = uuidgen.uuid('abcd', 0)

    with pytest.raises(ValueError):
        uuids = uuidgen.uuid_bulk(10, 'abc', 2)
