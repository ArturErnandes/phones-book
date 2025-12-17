#Файл с функционалом взаимодействия с БД



engine = create_async_engine(f'postgresql+asyncpg://postgres:{db_pass}@localhost:{db_port}/contacts_mai')

new_session = async_sessionmaker(engine, expire_on_commit=False)

