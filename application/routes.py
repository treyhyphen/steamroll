from flask import request, render_template, make_response, redirect, session, url_for, send_from_directory, jsonify, g
from flask import current_app as app
from steam import webapi, steamid

@app.before_request
def before_request_func():
    base_url = request.base_url
    if 'X-Forwarded-Host' in request.headers:
        base_url = f"https://{request.headers.get('X-Forwarded-Host')}"

    base_url_parts = base_url.split('/')
    if len(base_url_parts) > 3:
        base_url = '/'.join(base_url_parts[:3])

    g.base_url = base_url

@app.route('/', methods=['GET'])
@app.route('/<profile>')
def index(profile=None):
    return render_template('wrapper.html', profile=profile)

@app.route('/games/<profile>', methods=['GET'])
def games(profile=None):

    steam_api = webapi.WebAPI(app.config['STEAM_API_KEY'])

    user = steamid.SteamID(profile)
    if not user.id:
        user = steamid.from_url('https://steamcommunity.com/id/' + profile)
        
    if not user or not user.id:
        return make_response('Profile not found.', 404)

    profile = steam_api.call(
        'ISteamUser.GetPlayerSummaries',
        steamids=user.as_64,
        format='json'
    )

    if profile and 'response' in profile:
        profile = profile['response']['players'][0]
    else:
        profile = {}

    games = steam_api.call(
        'IPlayerService.GetOwnedGames',
        steamid=user.as_64,
        include_appinfo=True,
        include_played_free_games=False,
        appids_filter=None,
        include_free_sub=False,
        format='json'
    )

    max_playtime = 0
    for game in games['response']['games']:
        if game['playtime_forever'] > max_playtime:
            max_playtime = game['playtime_forever']

    games['response']['max_playtime'] = max_playtime

    return jsonify({'games': games['response'], 'profile': profile})

def lambda_handler(event, context):
    """Handle lambda requests."""
    return awsgi.response(app, event, context)
