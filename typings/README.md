# Contributor library typing

Scikit-learn 1.9.1 ships neither typing stubs nor a `py.typed` marker.
The local stub describes the public `train_test_split` arguments and preservation
of each input array's container type. It lets strict mypy check toolkit calls
without suppressing missing-import checks or adding untyped import adapters.
Only that public API is declared. Native behavior is verified through
`tests/integration/test_splitting.py`; this stub implements no runtime behavior
and is not installed in the toolkit wheel.

PyArrow 25 also has no typing marker. Its public `ArrowException` base is
declared for the native serialization failure assertion. The assertion uses
the real installed exception at runtime.

Review the signature and remove or replace these stubs when the supported
scikit-learn line supplies compatible typing. The owning evidence is
`docs/verification/us-12-19-ip3.md`.
