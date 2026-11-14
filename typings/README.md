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

US-15 IP2 adds the public BaseEstimator.get_params, clone, Pipeline,
ColumnTransformer, SimpleImputer, StandardScaler and OneHotEncoder surfaces
used by training-only fitting and its public tests. Constructors preserve the
reviewed native keyword arguments; fit/transform inputs are typed for positional
use only. Native output containers vary with composition/output settings, so
these third-party return types use Any; toolkit inputs and return records retain
explicit types and runtime shape/dtype validation. These contributor stubs do not
claim complete sklearn typing, alter runtime behavior, ship in the wheel or
disable any checker. Remove/replace them when upstream supplies typing.
