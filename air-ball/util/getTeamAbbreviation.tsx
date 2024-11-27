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
      "San Antonio Spurs": "SAS",
      "Toronto Raptors": "TOR",
      "Utah Jazz": "UTH",
      "Washington Wizards": "WAS"
    };
  
    return teamMap[teamName] || "Unknown Team";
  }

  export function getTeamImage(teamName: string): string {
    const teamMap: { [key: string]: string } = {
      "New York Knicks":"https://upload.wikimedia.org/wikipedia/fr/3/34/Knicks_de_NY.png",
      "Phoenix Suns":"https://upload.wikimedia.org/wikipedia/fr/5/56/Phoenix_Suns_2013.png",
      "Golden State Warriors":"https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Warriors_de_Golden_State_logo.svg/1200px-Warriors_de_Golden_State_logo.svg.png",
      "Milwaukee Bucks":"https://upload.wikimedia.org/wikipedia/fr/thumb/1/15/Milwaukee_Bucks_2015.svg/langfr-1024px-Milwaukee_Bucks_2015.svg.png",
      "Boston Celtics":"https://upload.wikimedia.org/wikipedia/fr/thumb/6/65/Celtics_de_Boston_logo.svg/1024px-Celtics_de_Boston_logo.svg.png",
      "Toronto Raptors":"https://upload.wikimedia.org/wikipedia/fr/8/89/Raptors2015.png",
      "Chicago Bulls":"https://upload.wikimedia.org/wikipedia/fr/thumb/d/d1/Bulls_de_Chicago_logo.svg/1200px-Bulls_de_Chicago_logo.svg.png",
      "Miami Heat":"https://upload.wikimedia.org/wikipedia/en/thumb/f/fb/Miami_Heat_logo.svg/1024px-Miami_Heat_logo.svg.png",
      "LA Clippers":"https://upload.wikimedia.org/wikipedia/fr/d/d6/Los_Angeles_Clippers_logo_2010.png",
      "Oklahoma City Thunder":"https://upload.wikimedia.org/wikipedia/en/thumb/5/5d/Oklahoma_City_Thunder.svg/1920px-Oklahoma_City_Thunder.svg.png",
      "Utah Jazz":"https://upload.wikimedia.org/wikipedia/fr/3/3b/Jazz_de_l%27Utah_logo.png",
      "Sacramento Kings":"https://upload.wikimedia.org/wikipedia/fr/thumb/9/95/Kings_de_Sacramento_logo.svg/1200px-Kings_de_Sacramento_logo.svg.png",
      "San Antonio Spurs":"https://upload.wikimedia.org/wikipedia/fr/0/0e/San_Antonio_Spurs_2018.png",
      "Dallas Mavericks":"https://upload.wikimedia.org/wikipedia/fr/thumb/b/b8/Mavericks_de_Dallas_logo.svg/150px-Mavericks_de_Dallas_logo.svg.png",
      "Orlando Magic":"https://upload.wikimedia.org/wikipedia/fr/b/bd/Orlando_Magic_logo_2010.png",
      "Houston Rockets":"https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Houston_Rockets_logo_2003.png/330px-Houston_Rockets_logo_2003.png",
      "Philadelphia 76ers":"https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg",
      "Los Angeles Lakers":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png",
      "Charlotte Hornets":"https://upload.wikimedia.org/wikipedia/fr/thumb/f/f3/Hornets_de_Charlotte_logo.svg/1200px-Hornets_de_Charlotte_logo.svg.png",
      "Cleveland Cavaliers":"https://upload.wikimedia.org/wikipedia/fr/thumb/0/06/Cavs_de_Cleveland_logo_2017.png/150px-Cavs_de_Cleveland_logo_2017.png",
      "Memphis Grizzlies":"https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Memphis_Grizzlies.svg/1200px-Memphis_Grizzlies.svg.png",
      "Indiana Pacers":"https://upload.wikimedia.org/wikipedia/fr/thumb/c/cf/Pacers_de_l%27Indiana_logo.svg/1180px-Pacers_de_l%27Indiana_logo.svg.png",
      "Detroit Pistons":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Logo_of_the_Detroit_Pistons.png/300px-Logo_of_the_Detroit_Pistons.png",
      "Brooklyn Nets":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Brooklyn_Nets_newlogo.svg/130px-Brooklyn_Nets_newlogo.svg.png",
      "New Orleans Pelicans":"https://upload.wikimedia.org/wikipedia/fr/thumb/2/21/New_Orleans_Pelicans.png/200px-New_Orleans_Pelicans.png",
      "Atlanta Hawks":"https://upload.wikimedia.org/wikipedia/fr/e/ee/Hawks_2016.png",
      "Denver Nuggets":"https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png",
      "Washington Wizards":"https://upload.wikimedia.org/wikipedia/fr/archive/d/d6/20161212034849%21Wizards2015.png",
      "Minnesota Timberwolves":"https://upload.wikimedia.org/wikipedia/fr/thumb/d/d9/Timberwolves_du_Minnesota_logo_2017.png/200px-Timberwolves_du_Minnesota_logo_2017.png",
      "Portland Trail Blazers":"https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Portland_Trail_Blazers_logo.svg/1200px-Portland_Trail_Blazers_logo.svg.png",
    };
  
    return teamMap[teamName] || "Unknown Team";
  }