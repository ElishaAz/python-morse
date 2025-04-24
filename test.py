from d2a import D2A
from a2d import A2D

def test(d2a: D2A, a2d: A2D, message: str):
    message = message.upper()
    d2a.reset()
    a2d.reset()
    d2a.encode(message)
    a2d.read_samples(d2a.get_samples())
    assert a2d.decode() == message, F"{a2d.decode()} == {message}"

if __name__ == '__main__':
    d2a = D2A()
    a2d = A2D()

    test(d2a, a2d, "Hello World")
    test(d2a, a2d, "Goodbye")

