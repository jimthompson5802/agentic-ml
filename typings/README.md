# Contributor library typing

Scikit-learn 1.9.1 ships neither typing stubs nor a `py.typed` marker.
The local stub describes the public `train_test_split` arguments and preservation
of each input array's container type. It lets strict mypy check toolkit calls
without suppressing missing-import checks or adding untyped import adapters.
The additional reviewed public surfaces are listed below. Native behavior is verified through
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

Phase 3 preprocessing coverage adds native `Pipeline.set_output` and NumPy integer
`OneHotEncoder.max_categories` settings. These describe exercised native public
APIs; they do not add product behavior, a runtime type dependency, or suppressions.

US-26 integration adds public Pipeline.get_feature_names_out and check_is_fitted.
BaseEstimator.get_params returns dict[str, object], preserving strict inspection
for both producer and consumer. See docs/verification/us-26-recording-ip3.md.

US-18 IP3 adds the native `accuracy_score` signature used by the project-owned
training example. Its array-like inputs are declared as object because this
bounded stub does not duplicate sklearn's input validator. It introduces no
runtime behavior or checker suppression and does not ship in the toolkit wheel.

US-14 IP2 adds `zero_one_loss` with the reviewed installed sklearn 1.9.1 signature
(`normalize=True`, `sample_weight=None`). Native accuracy/loss direction tests
exercise this public function. The same array-like typing rationale applies;
this is a contributor declaration, not a runtime wrapper or suppression.
