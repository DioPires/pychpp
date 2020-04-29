import datetime

from pychpp import ht_model
from pychpp import ht_xml
from pychpp import ht_team, ht_match


class HTMatchesArchive(ht_model.HTModel):
    """
    Hattrick matches archive
    """

    _SOURCE_FILE = "matchesarchive"
    _SOURCE_FILE_VERSION = "1.4"
    _REQUEST_ARGS = dict()

    _HT_ATTRIBUTES = [("team_id", "Team/TeamID", ht_xml.HTXml.ht_int),
                      ("team_name", "Team/TeamName", ht_xml.HTXml.ht_str),
                      ("first_match_date", "Team/FirstMatchDate", ht_xml.HTXml.ht_date_from_text),
                      ("last_match_date", "Team/LastMatchDate", ht_xml.HTXml.ht_date_from_text),
                      ]

    def __init__(self, ht_id=None, youth=False, first_match_date=None,
                 last_match_date=None, season=None, hto=False, **kwargs):

        # Check parameters integrity
        if not isinstance(ht_id, int) and ht_id is not None:
            raise ValueError("ht_id must be None or an integer")
        elif not isinstance(youth, bool):
            raise ValueError("youth must be a boolean")
        elif not isinstance(first_match_date, datetime.datetime) and first_match_date is not None:
            raise ValueError("first_match_date must be a datetime instance")
        elif not isinstance(last_match_date, datetime.datetime) and last_match_date is not None:
            raise ValueError("last_match_date must be a datetime instance")
        elif not isinstance(season, int) and season is not None:
            raise ValueError("season must be a integer")
        elif not isinstance(hto, bool):
            raise ValueError("hto must be a boolean")

        # Define request arguments
        self._REQUEST_ARGS["teamID"] = str(ht_id) if ht_id is not None else ""
        self._REQUEST_ARGS["isYouth"] = "true" if youth is True else "false"
        self._REQUEST_ARGS["FirstMatchDate"] = (ht_xml.HTXml.ht_date_to_text(first_match_date)
                                                if first_match_date is not None else "")
        self._REQUEST_ARGS["LastMatchDate"] = (ht_xml.HTXml.ht_date_to_text(last_match_date)
                                               if last_match_date is not None else "")
        self._REQUEST_ARGS["season"] = str(season) if season is not None else ""
        self._REQUEST_ARGS["HTO"] = "true" if hto is True else "false"

        super().__init__(**kwargs)

        self.matches_list = [HTMatchesArchiveItem(chpp=self._chpp, data=data)
                             for data in self._data.findall("Team/MatchList/Match")]

    def __getitem__(self, item):
        return self.matches_list[item]

    def __len__(self):
        return len(self.matches_list)

    def __repr__(self):
        return self.matches_list.__repr__()


class HTMatchesArchiveItem(ht_model.HTModel):
    """
    Object returned by HTMatchesArchve.search method
    """

    _HT_ATTRIBUTES = [("ht_id", "MatchID", ht_xml.HTXml.ht_int,),
                      ("home_team_id", "HomeTeam/HomeTeamID", ht_xml.HTXml.ht_int,),
                      ("home_team_name", "HomeTeam/HomeTeamName", ht_xml.HTXml.ht_str,),
                      ("away_team_id", "AwayTeam/AwayTeamID", ht_xml.HTXml.ht_int,),
                      ("away_team_name", "AwayTeam/AwayTeamName", ht_xml.HTXml.ht_str,),
                      ("date", "MatchDate", ht_xml.HTXml.ht_date_from_text,),
                      ("type", "MatchType", ht_xml.HTXml.ht_int,),
                      ("context_id", "MatchContextId", ht_xml.HTXml.ht_int,),
                      ("rule_id", "MatchRuleId", ht_xml.HTXml.ht_int,),
                      ("cup_level", "CupLevel", ht_xml.HTXml.ht_int,),
                      ("cup_level_index", "CupLevelIndex", ht_xml.HTXml.ht_int,),
                      ("home_goals", "HomeGoals", ht_xml.HTXml.ht_int,),
                      ("away_goals", "AwayGoals", ht_xml.HTXml.ht_int,),
                      ]

    def __repr__(self):
        return f"<{self.__class__.__name__} object : {self.home_team_name} - {self.away_team_name} ({self.ht_id})>"

    @property
    def details(self):
        return ht_match.HTMatch(chpp=self._chpp, ht_id=self.ht_id)

    @property
    def home_team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.home_team_id)

    @property
    def away_team(self):
        return ht_team.HTTeam(chpp=self._chpp, ht_id=self.away_team_id)