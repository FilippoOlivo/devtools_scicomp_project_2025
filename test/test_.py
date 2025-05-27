import pytest
from pyclassify.utils import distance, majority_vote
from pyclassify import kNN

@pytest.mark.parametrize(
    "point1, point2, point3, point4",
    [
        ([.1,2.,1.], [.1,2.,1.],[.1,2.,1.], [-1.,2.,5]),
        ([4.,2.,6.], [-1.,3.,0],[-.3,8.,1.],[-1.,2.,5]),
        ([4.,2.,6.,8.], [-1.,3.,0,1.], [-.3,8.,1.,12.],[-1.,2.,5, -8.])
    ]
)
def test_distance(point1, point2, point3, point4):
    d = distance(point1=point1, point2=point2)
    d_sym = distance(point1=point1, point2=point2)
    assert d >= 0
    assert d == d_sym

    d_12 = distance(point1=point1, point2=point2)
    d_13 = distance(point1=point1, point2=point3)
    d_23 = distance(point1=point2, point2=point3)
    assert d_12 + d_13 >= d_23

    d_14 = distance(point1=point1, point2=point4)
    d_24 = distance(point1=point2, point2=point4)
    d_34 = distance(point1=point3, point2=point4)
    assert d_12*d_34 + d_23 * d_14 >= d_13 * d_24

def test_wrong_distance():
    with pytest.raises(RuntimeError):
        distance([.1,.2,.3], [.1,.2,3, 4])

def test_majority_vote():
    y = [1, 0, 0, 1 ]
    assert majority_vote(y) == 1
    y = [1, 1, 0, 1 ]
    assert majority_vote(y) == 1
    y = [1, 0, 0, 0 ]
    assert majority_vote(y) == 0

def test_constructor():
    kNN(3)

def test_wrong_constructor():
    with pytest.raises(RuntimeError):
        kNN(-1)
    with pytest.raises(RuntimeError):
        kNN(1.1)