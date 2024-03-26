import psycopg2

class ActorCRUD:
  def __init__(self, dbname, user, password, host='localhost'):
    self.conn_params = {
      'dbname': dbname,
      'user': user,
      'password': password,
      'host': host
    }
    self.conn = None
    self.connect()

  def connect(self):
    try:
      self.conn = psycopg2.connect(**self.conn_params) # **kwargs로 전달됨, kwargs는 keyword argument의 줄임말로, 딕셔너리 그대로 함수로 전달됨.
      print("데이터베이스에 연결 성공")
    except psycopg2.Error as e:
      print(f"데이터베이스 연결 중 오류 발생: {e}")

  def create_actor(self, first_name, last_name):
    with self.conn.cursor() as cur:
      cur.execute("""
          INSERT INTO actor (first_name, last_name)
          VALUES (%s, %s) RETURNING actor_id;
          """, (first_name, last_name)) # 튜플로 값을 전달할 때는 항목 뒤에 콤마를 붙여 튜플임을 명시
      actor_id = cur.fetchone()[0] # 무슨 의미지?
      self.conn.commit()
      print(f"{first_name} {last_name} is successfully added as {actor_id}")
      return(actor_id)
  
  def read_actor(self, actor_id):
    with self.conn.cursor() as cur:
      cur.execute("""SELECT * FROM actor WHERE actor_id = %s;""", (actor_id,))
      actor = cur.fetchone()
      if actor:
        print(actor)
        return(actor)
      else:
        print("No such actor")
        return None
  
  def update_actor(self, first_name, last_name, rfirst_name, rlast_name):
    with self.conn.cursor() as cur:
      cur.execute(f"""
                  UPDATE actor SET first_name = '{rfirst_name}', last_name = '{rlast_name}'
                  WHERE first_name = '{first_name}' and last_name = '{last_name}'""")
      self.conn.commit()
      print(f"배우 {first_name} {last_name}의 정보가 {rfirst_name} {rlast_name}로 업데이트 됨.")
  
  def delete_actor(self, actor_id):
    with self.conn.cursor() as cur:
      try:
        cur.execute(f"""
            DELETE FROM actor WHERE actor_id = ({actor_id});""")
        self.conn.commit()
        print(f"{actor_id}번 배우의 정보가 삭제됨.")
      except:
        print("데이터 삭제 시 오류 발생")
  
  def recommendation(self):
    with self.conn.cursor() as cur:
      cur.execute(f"""
          select title from film
          order by random()
          fetch first 3 row only;""")
      title = cur.fetchone()
      return title


  def close(self):
    if self.conn:
      self.conn.close()
      print('database was closed.')


actor_crud = ActorCRUD()
# actor_id = actor_crud.create_actor('Olivia', 'rendler')
# actor_crud.read_actor(35)
# actor_crud.delete_actor(22)
# actor_crud.update_actor('Mickey', 'Mouse', 'Thora', 'Temple')
print(actor_crud.recommendation())

