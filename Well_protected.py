"""

   For the API calls below, no authentication is needed. You'll just need to have your
   Bungie API key exported in your bash profile
   and named as BUNGIE_API_KEY to run the script as-is.
   """
import os
import requests

# make sure you set your API Key in Your environment
API_ROOT = "https://bungie.net/Platform"
BUNGIE_API_KEY = os.environ["BUNGIE_API_KEY"]
HEADERS = {"X-API-Key": BUNGIE_API_KEY}

# Put your PSN ID here
PSN_ID = "KH4L3D-TH3-GR348"


class BungieData(object):

    def __init__(self, api_key):
        """

        api_key (str): The api key given to you by Bungie when you registered your app with them
        """
        self.api_key = api_key

    def get_manifest(self):
        site_call = API_ROOT + "/Destiny2/Manifest/"
        request = requests.get(site_call, headers=HEADERS)
        return request.json()['Response']

    def get_player_by_tag_name(self, gamertag):
        """

        Gamertag (str): The PSN gamertag a player uses on Destiny 2.
        """
        site_call = API_ROOT + "/Destiny2/SearchDestinyPlayer/2/" + gamertag
        request = requests.get(site_call, headers=HEADERS)
        return request.json()['Response']

    def get_destiny_user_id(self, gamertag):
        """

        Uses old Destiny endpoint for a PSN user to get the BUNGIE membershipId
        Gamertag (str): The PSN gamertag a player uses on Destiny 2.
        """
        info = self.get_player_by_tag_name(gamertag)
        return int(info[0]['membershipId'])

    def get_destiny_user_profile(self, membership_id, components=[100]):
        """.

        membership_id (int): the Destiny membership_id of a player. (returned by get_Destiny_user_id)
        components (list of ints):
        the type of info you want returned according the Bungie API docs.
        Defaults to 100: basic profile info ([100, 200] would also return more detailed info
        by Destiny character
        """
        components = "?components=" + ','.join([str(c) for c in components])
        site_call = API_ROOT + "/Destiny2/2/Profile/" + str(membership_id) + "/" + components
        request = requests.get(site_call, headers=HEADERS)
        return request.json()['Response']['profile']['data']

    def get_bungie_user_id(self, membership_id):
        """.

        membership_id (int): the Destiny membership_id of a player. (returned by get_Destiny_user_id)
        """
        site_call = API_ROOT + "/User/GetMembershipsById/" + str(membership_id) + "/2/"
        request = requests.get(site_call, headers=HEADERS)
        return int(request.json()['Response']['bungieNetUser']['membershipId'])

    def get_profile_info(self, gamertag):
        """

        :param gamertag: Your PSN ID.
        :return:
        """
        # Get stuff
        membership_id = self.get_destiny_user_id(gamertag)
        profile = self.get_destiny_user_profile(membership_id)
        bungie_membership_id = self.get_bungie_user_id(membership_id)

        # Print stuff
        print("PSN ID: {}".format(PSN_ID))
        print("My's Destiny Membership ID: {}".format(membership_id))
        print("My's Bungie.net Membership ID: {}".format(bungie_membership_id))
        print("-----------------")
        return profile

    def get_character_by_id(self, membership_id, character_id, components=[200]):
        """

        :param membership_id: the Destiny membership_id of a player.
        :param character_id: the character ID you passed.
        :param components:
            Characters: 200
            CharacterInventories: 201
            CharacterProgressions: 202
            CharacterActivities: 204
            CharacterEquipment: 205
            Kiosks: 500

        :return:
        """

        components = "?components=" + ','.join([str(c) for c in components])
        site_call = "https://bungie.net/Platform/Destiny2/2/profile/" + str(membership_id) + \
                    "/Character/" + character_id + components
        request = requests.get(site_call, headers=HEADERS)
        return request.json()['Response']['character']['data']


if __name__ == '__main__':
    # Never put your keys in code... export 'em!
    bungie = BungieData(api_key=BUNGIE_API_KEY)
    your_membership_id = bungie.get_destiny_user_id(PSN_ID)
    your_profile = bungie.get_profile_info(PSN_ID)

    # Characters
    first_character = your_profile['characterIds'][0]
    second_character = your_profile['characterIds'][1]
    third_character = your_profile['characterIds'][2]

    # set Character and Components
    character = bungie.get_character_by_id(your_membership_id, first_character)

    # # Get User's Profile info and more detailed Character info
    print("Your Character Info: \n{}".format(character))

