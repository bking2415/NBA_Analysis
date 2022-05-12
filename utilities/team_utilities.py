def getTeamInfo(soup):
    # Fetching Team Name and City items
    html_type = "div"
    header = "nba-team-header__team-location"
    team_data = soup.find_all(html_type, header)
    # print(team_data)

    # Loop through team names
    for val in team_data:
        # Extracting Team City
        teamCity = val.find('p', attrs={'class': 'nba-team-header__city-name'}).text
        # print(teamCity)
        teamMascot = val.find('p', attrs={'class': 'nba-team-header__team-name'}).text
        # print(teamMascot)

    return [teamCity, teamMascot]
