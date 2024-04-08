export function getTeamAbbreviation(teamName: string): string {
    const teamMap: { [key: string]: string } = {
      "Atlanta Hawks": "ATL",
      "Boston Celtics": "BOS",
      "Charlotte Hornets": "CHA",
      "Chicago Bulls": "CHI",
      "Cleveland Cavaliers": "CLE",
      "Dallas Mavericks": "DAL",
      "Denver Nuggets": "DEN",
      "Detroit Pistons": "DET",
      "Golden State Warriors": "GSW",
      "Houston Rockets": "HOU",
      "Indiana Pacers": "IND",
      "LA Clippers": "LAC",
      "Los Angeles Lakers": "LAL",
      "Memphis Grizzlies": "MEM",
      "Miami Heat": "MIA",
      "Milwaukee Bucks": "MIL",
      "Minnesota Timberwolves": "MIN",
      "New Orleans Pelicans": "NOH",
      "New York Knicks": "NYK",
      "Brooklyn Nets": "BKN",
      "Oklahoma City Thunder": "OKC",
      "Orlando Magic": "ORL",
      "Philadelphia 76ers": "PHI",
      "Phoenix Suns": "PHO",
      "Portland Trail Blazers": "POR",
      "Sacramento Kings": "SAC",
      "Toronto Raptors": "TOR",
      "Utah Jazz": "UTH",
      "Washington Wizards": "WAS"
    };
  
    return teamMap[teamName] || "Unknown Team";
  }

  export function getTeamImage(teamName: string): string {
    const teamMap: { [key: string]: string } = {
      "Atlanta Hawks": "ATL",
      "Boston Celtics": "BOS",
      "Charlotte Hornets": "CHA",
      "Chicago Bulls": "CHI",
      "Cleveland Cavaliers": "CLE",
      "Dallas Mavericks": "DAL",
      "Denver Nuggets": "DEN",
      "Detroit Pistons": "DET",
      "Golden State Warriors": "GSW",
      "Houston Rockets": "HOU",
      "Indiana Pacers": "IND",
      "LA Clippers": "LAC",
      "Los Angeles Lakers": "LAL",
      "Memphis Grizzlies": "MEM",
      "Miami Heat": "MIA",
      "Milwaukee Bucks": "MIL",
      "Minnesota Timberwolves": "MIN",
      "New Orleans Pelicans": "NOH",
      "New York Knicks": "NYK",
      "Brooklyn Nets": "BKN",
      "Oklahoma City Thunder": "OKC",
      "Orlando Magic": "ORL",
      "Philadelphia 76ers": "PHI",
      "Phoenix Suns": "PHO",
      "Portland Trail Blazers": "POR",
      "Sacramento Kings": "SAC",
      "Toronto Raptors": "TOR",
      "Utah Jazz": "UTH",
      "Washington Wizards": "WAS"
    };
  
    return teamMap[teamName] || "Unknown Team";
  }