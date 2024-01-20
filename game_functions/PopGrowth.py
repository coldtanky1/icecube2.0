import sqlite3

def popgrowth(user_id):
    try:
        conn = sqlite3.connect('player_info.db')
        cursor = conn.cursor()

        # fetch user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            nation_name = result[0]
            
            # fetch user's production infra
            cursor.execute(
                'SELECT name, nation_score, gdp, child, teen, adult, elder, balance FROM user_stats WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            if infra_result:
                name, nation_score, gdp, child, teen, adult, elder, balance = infra_result

                # Growth factors for each age group
                child_growth_factor = 0.02  # Example growth factor for children, Over time we can make this change dynamically
                teen_growth_factor = 0.02   # Example growth factor for teens, Over time we can make this change dynamically
                adult_growth_factor = 0.01  # Example growth factor for adults, Over time we can make this change dynamically
                elder_growth_factor = 0.005  # Example growth factor for elders, Over time we can make this change dynamically

                # Calculate growth for each age group with the growth factor
                child_growth = int(child * child_growth_factor)
                teen_growth = int(teen * teen_growth_factor)
                adult_growth = int(adult * adult_growth_factor)
                elder_growth = int(elder * elder_growth_factor)

                # Growth for each age group each turn.
                child_next_turn = child + child_growth
                teen_next_turn = teen + child_growth
                adult_next_turn = adult + adult_growth
                elder_next_turn = elder + elder_growth

                # Update the pop values.
                cursor.execute('UPDATE user_stats SET child = ?, teen = ?, adult = ?, elder = ? WHERE name = ?',
                                (child_next_turn, teen_next_turn, adult_next_turn, elder_next_turn, nation_name))
                conn.commit()
            else:
                print("error getting stats.")
                return

        else:
            print(f"An error happened when trying to update PopGrowth for player {nation_name}.")
            return
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print("Details:", e.args)
        conn.rollback()
    finally:
        conn.close()