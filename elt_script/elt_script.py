import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay_seconds = 6):
    for _ in range(max_retries):
        try:
            result = subprocess.run(["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print(f"Succesfully connected to the host: {host}")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to Postgres: {e}")
            time.sleep(delay_seconds)

    print("Max retries reached")
    return False

def main():
    if not wait_for_postgres(host="source_postgres"):
        exit(1)

    print("Starting ELT operation")

    source_config = {
        'dbname': 'source_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'source_postgres'
    }

    destination_config = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'destination_postgres'
    }

    dump_cmd = [
        'pg_dump',
        '-h', source_config['host'],
        '-U', source_config['user'],
        '-d', source_config['dbname'],
        '-f', 'data_dump.sql',
        '-w'
    ]

    subprocess_env = dict(PGPASSWORD=source_config['password'])
    subprocess.run(dump_cmd, env=subprocess_env, check=True)

    load_cmd = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['dbname'],
        '-a', '-f', 'data_dump.sql'
    ]

    subprocess_env = dict(PGPASSWORD=destination_config['password'])
    subprocess.run(load_cmd, env=subprocess_env, check=True)

    print("Ending ELT script...")

if __name__ == "__main__":
    main()