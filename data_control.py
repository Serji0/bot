import MySQLdb



class Connection:
    def __init__(self, user, password, db, host='localhost'):
        self.user = user
        self.host = host
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self._connection = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.db,
            use_unicode=True,
            charset='utf8'
        )

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def add_user(self, id, q, b):
        self.connect()
        c = self.connection.cursor()
        c.execute("INSERT INTO app_user (telegram_id, qiwi, balance) VALUES (%s, %s, %s);", (id, q, b))
        self.connection.commit()
        c.close()
        self.disconnect()

    def get_bets(self, id):
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT id from app_user WHERE telegram_id = %s', (str(id),))
        u_id = c.fetchone()
        c.execute("SELECT * from app_bet WHERE user_id = %s", (u_id,))
        bets = c.fetchall()
        c.close()
        self.disconnect()
        return bets

    def get_event_by_id(self, id):
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT * from app_event WHERE id = %s', (str(id),))
        event = c.fetchone()
        c.close()
        self.disconnect()
        return event

    def get_user_by_telegram_id(self, id):
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT * from app_user WHERE telegram_id = %s', (str(id),))
        user = c.fetchone()
        c.close()
        self.disconnect()
        return user

    def get_leagues_by_sport(self, sport):
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT league from app_team WHERE sport = %s', (str(sport),))
        leagues = c.fetchall()
        leagues1 = []
        for league in leagues:
            leagues1.append(league[0])
        leagues = list(set(leagues1))
        c.close()
        self.disconnect()
        return leagues

    def get_events_by_league(self, league):
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT * from app_event WHERE league = %s and status = %s', (str(league), 'active'))
        events = c.fetchall()
        events1 = []
        for event in events:
            ev = str(event[3]) + ' - ' + str(event[4])
            events1.append(ev)
        c.close()
        self.disconnect()
        return events1

    def get_sports(self):
        self.connect()
        c = self._connection.cursor()
        c.execute('SELECT sport from app_team')
        sports = c.fetchall()
        sports1 = []
        for sport in sports:
            sports1.append(sport[0])
        sports = list(set(sports1))
        c.close()
        self.disconnect()
        return sports

    def get_ratios_by_teams(self, teams):
        s = teams.find(' - ')
        team1 = teams[:s]
        team2 = teams[s + 3:]
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT * from app_event WHERE team1 = %s AND team2 = %s', (str(team1), str(team2)))
        event = list(c.fetchone())
        events1 = []
        buf = 'П1 - ' + str(event[6])
        events1.append([buf])
        buf = 'X - ' + str(event[7])
        events1.append([buf])
        buf = 'П2 - ' + str(event[8])
        events1.append([buf])
        buf = 'ТМ' + str(event[9]) + ' - ' + str(event[10])
        events1.append([buf])
        buf = 'ТБ' + str(event[9]) + ' - ' + str(event[11])
        events1.append([buf])
        c.close()
        self.disconnect()
        return events1

    def get_maxbet_by_teams(self, teams):
        s = teams.find(' - ')
        team1 = teams[:s]
        team2 = teams[s + 3:]
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT max_bet from app_event WHERE team1 = %s AND team2 = %s', (str(team1), str(team2)))
        maxbet = c.fetchone()[0]
        self.disconnect()
        return maxbet

    def get_event_id_by_teams(self, teams):
        s = teams.find(' - ')
        team1 = teams[:s]
        team2 = teams[s + 3:]
        self.connect()
        c = self.connection.cursor()
        c.execute('SELECT id from app_event WHERE team1 = %s AND team2 = %s', (str(team1), str(team2)))
        id = c.fetchone()[0]
        self.disconnect()
        return id

    def get_bets_by_user_event_choice(self, u_id, e_id, choice):
        self.connect()
        c = self.connection.cursor()
        user = self.get_user_by_telegram_id(u_id)[0]
        c.execute('SELECT * from app_bet WHERE user_id = %s AND event_id = %s AND choice = %s',
                  (str(user), str(e_id), str(choice)))
        bets = (c.fetchall())
        return bets

    def add_bet(self, id, teams, choice, sum):

        max = self.get_maxbet_by_teams(teams)
        if float(sum) > max:
            response = 'Слишком большая сумма ставки'
        elif float(sum) < 5:
            response = 'Слишком маленькая сумма ставки'
        else:
            user = self.get_user_by_telegram_id(id)
            balance = float(user[2])
            if balance < float(sum):
                response = 'Недостаточно средств на счете'
            else:
                event = self.get_event_id_by_teams(teams)
                user_id = user[0]
                s = choice.find(' - ')
                pick = choice[:s]
                if pick == 'п1':
                    pick = 'win1'
                elif pick == 'х':
                    pick = 'draw'
                elif pick == 'п2':
                    pick = 'win2'
                elif 'тм' in pick:
                    pick = 'under'
                elif 'тб' in pick:
                    pick = 'over'

                bet = self.get_bets_by_user_event_choice(id, event, pick)
                if bet:
                    response = 'Вы уже сделали ставку на этот исход'
                else:
                    ratio = choice[s + 3:]
                    balance -= float(sum)
                    self.connect()
                    c = self.connection.cursor()
                    c.execute(
                        "INSERT INTO app_bet (event_id, user_id, amount, ratio, choice, status) VALUES (%s, %s, %s, %s, %s, %s);",
                        (event, user_id, sum, ratio, pick, 'unknown'))
                    self.connection.commit()
                    c.execute('UPDATE app_user SET balance = %s WHERE id = %s;', (str(balance), str(user_id)))
                    self.connection.commit()
                    c.close()
                    self.disconnect()
                    response = 'Ваша ставка принята'
        return response

    def add_request(self, id, comment, type):
        self.connect()
        user = self.get_user_by_telegram_id(id)
        user_id = user[0]
        c = self.connection.cursor()
        c.execute("INSERT INTO app_request (user_id, comment, type, status) VALUES (%s, %s, %s, %s);",
                  (user_id, comment, type, 'new'))
        self.connection.commit()
        self.disconnect()
        c.close()
