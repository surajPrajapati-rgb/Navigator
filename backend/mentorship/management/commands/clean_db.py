from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Clean the SQLite database by dropping all tables, except sqlite_sequence.'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Temporarily disable foreign key constraints
            cursor.execute("PRAGMA foreign_keys=OFF;")
            
            try:
                # Get all tables
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name != 'sqlite_sequence';
                """)
                tables = [table[0] for table in cursor.fetchall()]

                # Build dependency graph
                dependencies = {}
                for table in tables:
                    cursor.execute(f"PRAGMA foreign_key_list({table});")
                    foreign_keys = cursor.fetchall()
                    dependencies[table] = [fk[2] for fk in foreign_keys]  # fk[2] is the referenced table name

                # Topological sort to determine correct drop order
                drop_order = []
                visited = set()
                temp_visited = set()

                def topological_sort(table):
                    if table in temp_visited:
                        raise ValueError(f"Circular dependency detected involving table {table}")
                    if table not in visited:
                        temp_visited.add(table)
                        for dep_table in dependencies.get(table, []):
                            if dep_table in tables:  # Only process if the dependent table exists
                                topological_sort(dep_table)
                        temp_visited.remove(table)
                        visited.add(table)
                        drop_order.append(table)

                # Process all tables
                for table in tables:
                    if table not in visited:
                        topological_sort(table)

                # Drop tables in reverse order (most dependent first)
                for table in reversed(drop_order):
                    try:
                        cursor.execute(f"DROP TABLE IF EXISTS {table};")
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully dropped table: {table}')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error dropping table {table}: {str(e)}')
                        )

            finally:
                # Re-enable foreign key constraints
                cursor.execute("PRAGMA foreign_keys=ON;")

        self.stdout.write(
            self.style.SUCCESS('Database cleanup completed successfully.')
        )