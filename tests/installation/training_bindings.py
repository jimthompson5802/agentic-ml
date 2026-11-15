"""Project-owned native bindings; adding a forest needs no toolkit change."""

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

ESTIMATOR_BINDINGS = {
    "dummy_classifier": DummyClassifier,
    "decision_tree": DecisionTreeClassifier,
    "random_forest": RandomForestClassifier,
}
