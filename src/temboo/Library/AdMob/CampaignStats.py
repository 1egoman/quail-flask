# -*- coding: utf-8 -*-

###############################################################################
#
# CampaignStats
# Retrieve campaign stats by ID.
#
# Python versions 2.6, 2.7, 3.x
#
# Copyright 2014, Temboo Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class CampaignStats(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CampaignStats Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CampaignStats, self).__init__(temboo_session, '/Library/AdMob/CampaignStats')


    def new_input_set(self):
        return CampaignStatsInputSet()

    def _make_result_set(self, result, path):
        return CampaignStatsResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CampaignStatsChoreographyExecution(session, exec_id, path)

class CampaignStatsInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CampaignStats
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_CampaignID(self, value):
        """
        Set the value of the CampaignID input for this Choreo. ((required, string) Search for ad campaigns using this ID.)
        """
        super(CampaignStatsInputSet, self)._set_input('CampaignID', value)
    def set_ClientKey(self, value):
        """
        Set the value of the ClientKey input for this Choreo. ((required, string) The Client Key provided by AdMob.)
        """
        super(CampaignStatsInputSet, self)._set_input('ClientKey', value)
    def set_Email(self, value):
        """
        Set the value of the Email input for this Choreo. ((conditional, string) Your AdMob username. Required unless providing a valid Token input.)
        """
        super(CampaignStatsInputSet, self)._set_input('Email', value)
    def set_EndDate(self, value):
        """
        Set the value of the EndDate input for this Choreo. ((required, date) Enter search end date in following format: 2011-09-12)
        """
        super(CampaignStatsInputSet, self)._set_input('EndDate', value)
    def set_ObjectDimension(self, value):
        """
        Set the value of the ObjectDimension input for this Choreo. ((optional, string) Specify a campaign to group and narrow your search.)
        """
        super(CampaignStatsInputSet, self)._set_input('ObjectDimension', value)
    def set_OrderBy(self, value):
        """
        Set the value of the OrderBy input for this Choreo. ((optional, string) Order by the number of impressions. Example: [impressions]=asc)
        """
        super(CampaignStatsInputSet, self)._set_input('OrderBy', value)
    def set_Password(self, value):
        """
        Set the value of the Password input for this Choreo. ((conditional, password) Your Admob password. Required unless providing a valid Token input.)
        """
        super(CampaignStatsInputSet, self)._set_input('Password', value)
    def set_ResponseFormat(self, value):
        """
        Set the value of the ResponseFormat input for this Choreo. ((optional, string) The format that your want the response to be in. Accepted values are: xml (the default) and json.)
        """
        super(CampaignStatsInputSet, self)._set_input('ResponseFormat', value)
    def set_StartDate(self, value):
        """
        Set the value of the StartDate input for this Choreo. ((required, date) Enter search start date in following format: 2011-09-12)
        """
        super(CampaignStatsInputSet, self)._set_input('StartDate', value)
    def set_TimeDimension(self, value):
        """
        Set the value of the TimeDimension input for this Choreo. ((optional, string) Specify whether stats should be grouped by day, week, or month.)
        """
        super(CampaignStatsInputSet, self)._set_input('TimeDimension', value)
    def set_Token(self, value):
        """
        Set the value of the Token input for this Choreo. ((conditional, string) If provided, the Choreo will use the token to authenticate. If the token is expired or not provided, the Choreo will relogin and retrieve a new token when Email and Password are supplied.)
        """
        super(CampaignStatsInputSet, self)._set_input('Token', value)

class CampaignStatsResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CampaignStats Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from AdMob. Corresponds to the ResponseFormat input. Defaults to xml.)
        """
        return self._output.get('Response', None)
    def get_Token(self):
        """
        Retrieve the value for the "Token" output from this Choreo execution. ((conditional, string) If provided, the Choreo will use the token to authenticate. If the token is expired or not provided, the Choreo will relogin and retrieve a new token when Email and Password are supplied.)
        """
        return self._output.get('Token', None)

class CampaignStatsChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CampaignStatsResultSet(response, path)
