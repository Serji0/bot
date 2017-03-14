from data_control import Connection

con = Connection('root', 'root', 'betbot')

EPL = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
       'Hull City', 'Leister City', 'Liverpool', 'Manchester City', 'Manchester United', 'Middlesbrough',
       'Southampton', 'Stoke City', 'Sunderland', 'Swansey', 'Tottenham', 'Watford', 'West Bromwich',
       'West Ham']
Bundesliga = ['Augsburg', 'Bayer 04', 'Bayern', 'Borussia D.', 'Borussia M.', 'Darmstadt 98', 'Eintracht',
              'Freiburg', 'Hamburger SV', 'Herta', 'Hoffenheim 1899', 'Ingolstadt 04', 'Koln', 'Mainz 05',
              'RB Leipzig', 'Shalke 04', 'Wolfsburg', 'Werder']
LaLiga = ['Alaves', 'Athletic', 'Atletico', 'Celta', 'Deportivo', 'Eibar', 'Espanyol', 'FC Barcelona',
          'Granada', 'Las Palmas', 'Leganes', 'Malaga', 'Osasuna', 'R. Betis', 'R. Madrid', 'R. Sociedad',
          'Sevilla', 'Sporting', 'Valencia', 'Villareal']
Serie_A = ['Atalanta', 'Bologna', 'Cagliari', 'Chievoverona', 'Crotone', 'Empoli', 'Fiorentina', 'Genoa',
           'Inter', 'Juventus', 'Lazio', 'Milan', 'Napoli', 'Palermo', 'Pescara', 'Roma', 'Sampdoria',
           'Sassuolo', 'Torino', 'Udinese']
Ligue_1 = ['Angers', 'Bastia', 'Bordeaux', 'Caen', 'Dijon', 'Guingamp', 'LOSC', 'Lorient', 'OL', 'OM',
           'Metz', 'Monaco', 'Monpellier', 'Nancy', 'Nantes', 'Nice', 'PSG', 'Rennais', 'Saint-Etienne',
           'Toulouse']
RFPL = ['Amkar', 'Anji', 'Arsenal', 'CSKA', 'Krasnodar', 'Krylia sovetov', 'Lokomotiv', 'Orenburg',
        'Rostov', 'Rubin', 'Spartak', 'Terek', 'Tom', 'UFA', 'Ural', 'Zenit'],
Ukraine_league = ['Chornomorets', 'Dnipro', 'Dynamo', 'Karpaty', 'Oleksandria', 'Olimpick', 'Shaktar',
                  'Stal Kamianske', 'Volyn', 'Vorskla', 'Zirka', 'Zorya']
FNL = ['Baltika', 'Dynamo', 'Enisey', 'Fakel', 'Himki', 'Kuban', 'Luch-energia', 'Mordovia', 'Neftehimik',
       'Shinnik', 'Sibir', 'SKA', 'Sokol', 'Spartak-2', 'Spartak-Nalchik', 'Tambov', 'Tosno', 'Tumen',
       'Volgar', 'Zenit-2']
Champions_league = ['Atletico', 'Barcelona', 'Bayer 04' 'Bayern', 'Borussia D.', 'Juventus', 'Leister',
                    'Manchester City', 'Monaco', 'Porto', 'Real Madrid', 'Sevilla']
Europa_league = ['Ajax', 'Anderlecht', 'APOEL', 'Besiktas', 'Borussia M.', 'Celta', 'Genk', 'Gent',
                 'Kobenhagen', 'Krasnodar', 'Lyon', 'Manchester United', 'Olimpiakos', 'Roma', 'Rostov',
                 'Shalke 04']
NBA = ['Atlanta', 'Boston', 'Brooklyn', 'Charlotte', 'Chicago', 'Cleveland', 'Dallas', 'Denver', 'Detroit',
       'Golden State', 'Houston', 'Indiana', 'LA Clippers', 'LA Lakers', 'Miami', 'Milwaukee', 'Minnesota',
       'New Orleans', 'New York', 'Okhlahoma', 'Orlando', 'Philadelphia', 'Phoenix', 'Portland',
       'Sacramento', 'San Antonio', 'Toronto', 'Utah', 'Washington']
NHL = ['Anaheim', 'Arizona', 'Boston', 'Buffalo', 'Calgary', 'Carolina', 'Chicago', 'Colorado', 'Columbus', 'Dallas',
       'Detroit','Edmonton', 'Florida', 'Las Angeles', 'Minnesota', 'Monreal', 'Nashville', 'New Jersey',
       'New York Islanders', 'New York Rangers', 'Philadelphia', 'Pittsburgh', 'San Jose', 'St. Louis', 'Tampa Bay',
       'Toronto', 'Vancouver', 'Washington', 'Winnipeg']
KHL = ['Ak Bars', 'Avangard' , 'Barys', 'CSKA', 'Dynamo Moscow', 'Lokomotiv', 'Metallurg Magnitogorsk', 'SKA']



con.connect()
c = con.connection.cursor()
for team in EPL:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'EPL', str(team)))
    c.connection.commit()
for team in LaLiga:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'LaLiga', str(team)))
    c.connection.commit()
for team in Serie_A:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Serie_A', str(team)))
    c.connection.commit()
for team in Bundesliga:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Bundeslig', str(team)))
    c.connection.commit()
for team in Ligue_1:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Ligue_1', str(team)))
    c.connection.commit()
for team in Ukraine_league:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Ukraine_league', str(team)))
    c.connection.commit()
for team in RFPL:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'RFPL', str(team)))
    c.connection.commit()
for team in FNL:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'FNL', str(team)))
    c.connection.commit()
for team in Europa_league:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Europa_league', str(team)))
    c.connection.commit()
for team in Champions_league:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('football', 'Champions_league', str(team)))
    c.connection.commit()
for team in KHL:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('hockey', 'KHL', str(team)))
    c.connection.commit()
for team in NHL:
    c.execute("INSERT INTO app_team (sport, league, name) VALUES (%s, %s, %s);", ('hockey', 'NHL', str(team)))
    c.connection.commit()
c.close()
con.disconnect()
