from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from datetime import datetime, timezone
@dataclass
class AccountVersion:
    """For a single version"""
    npm_maintainers: int = 0
    #'npm_maintainers_nicks': [],
    #'npm_maintainers_emails': [],
    #'npm_maintainer_published_release': '', #test
    #'github_contributors': 0,
    #'github_contributors_nicks': [],
    #'github_contributors_emails': [],
    npm_hash_commit: str = ""
    ##github_hash_commit: str = ""
    npm_release_date: Optional[datetime] = datetime.min.replace(tzinfo=timezone.utc) #None
    #'github_release_date': AccountAnalyzer.UTC_MIN_DATETIME,    # missing date, empty metrics

@dataclass
class AccountAggregate:
    """For aggregate versions"""
    avg_npm_maintainers: float = 0.0