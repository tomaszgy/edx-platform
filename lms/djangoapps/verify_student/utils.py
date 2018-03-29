# -*- coding: utf-8 -*-
"""
Utility functions for ID Verification.
"""

from datetime import datetime, timedelta
import pytz
from django.conf import settings


def is_verification_expiring_soon(expiration_datetime):
    """
    Returns True if verification is expiring within EXPIRING_SOON_WINDOW.
    """
    if expiration_datetime:
        if (expiration_datetime - datetime.now(pytz.UTC)).days <= settings.VERIFY_STUDENT.get(
                "EXPIRING_SOON_WINDOW"):
            return True

    return False


def earliest_allowed_verification_date():
    """
    Returns the earliest allowed date given the settings

    """
    days_good_for = settings.VERIFY_STUDENT["DAYS_GOOD_FOR"]
    return datetime.now(pytz.UTC) - timedelta(days=days_good_for)


def verification_for_datetime(deadline, candidates):
    """Find a verification in a set that applied during a particular datetime.

    A verification is considered "active" during a datetime if:
    1) The verification was created before the datetime, and
    2) The verification is set to expire after the datetime.

    Note that verification status is *not* considered here,
    just the start/expire dates.

    If multiple verifications were active at the deadline,
    returns the most recently created one.

    Arguments:
        deadline (datetime): The datetime at which the verification applied.
            If `None`, then return the most recently created candidate.
        candidates (list of `PhotoVerification`s): Potential verifications to search through.

    Returns:
        PhotoVerification: A photo verification that was active at the deadline.
            If no verification was active, return None.

    """
    if len(candidates) == 0:
        return None

    # If there's no deadline, then return the most recently created verification
    if deadline is None:
        return candidates[0]

    # Otherwise, look for a verification that was in effect at the deadline,
    # preferring recent verifications.
    # If no such verification is found, implicitly return `None`
    for verification in candidates:
        if verification.active_at_datetime(deadline):
            return verification
