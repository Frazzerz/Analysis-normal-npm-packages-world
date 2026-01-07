from dataclasses import dataclass
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol
@dataclass
class AccountChanges:
    package_reactivation: bool = False
    #npm_new_maintainer: bool
    #npm_awakening_inactive_maintainer: bool
    #npm_new_maintainer_published_first_time_releases: bool
    #github_new_contributors: bool
    #hash_mismatch_commit_between_npm_and_github: bool  # no more github hash commit collected
    #npm_before_github: bool            # test
    #anomalous_time: bool

    THRESHOLDS = [
        GenericThresholdRule(
            name="Package reactivation",
            metric_path="account.package_reactivation",
            config=ThresholdConfig(
                boolean=True,
                description="The package was reactivated in this version",
            ),
        ),
    ]