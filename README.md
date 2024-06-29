# ByteBelt
Install django 
pyenv install 3.12.1

python3 -m venv myvenv
source myvenv/bin/activate
python -m pip install django

python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt. /// firebase-admin
pip install autopep8 beautifulsoup4

https://realpython.com/django-setup/

Exulter dans une sandbox 
Un docker avec un worker avec un redis 
Sur un kube 



 # Set up the database && apres un ajout de model pour mettre a jour la base de donnee et toujours les executer dans le container docker
python manage.py makemigrations
python manage.py migrate

#set up userApi
pip install djangorestframework



INSERT INTO "userApi_customuser" (last_login, is_superuser, first_name, last_name, is_staff, date_joined, id, username, email, password, is_active, role, created_at, updated_at, profile_pic, bio) VALUES
('2024-06-21 01:10:10.000000+00', false, 'Jean', 'Dupont', false, '2024-06-21 01:10:10.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b772', 'jeand', 'jeandupont@gmail.com', 'password123', true, 'user', '2024-06-21 01:10:10.000000+00', '2024-06-21 01:10:10.000000+00', 'profile_pics/profile1.png', 'Loves cycling and photography'),
('2024-06-21 01:20:20.000000+00', false, 'Marie', 'Curie', false, '2024-06-21 01:20:20.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b773', 'mariec', 'mariecurie@gmail.com', 'securepass', true, 'user', '2024-06-21 01:20:20.000000+00', '2024-06-21 01:20:20.000000+00', 'profile_pics/profile2.png', 'Physics and Chemistry enthusiast'),
('2024-06-21 01:30:30.000000+00', false, 'Albert', 'Einstein', false, '2024-06-21 01:30:30.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b774', 'alberte', 'alberteinstein@gmail.com', 'relativity', true, 'user', '2024-06-21 01:30:30.000000+00', '2024-06-21 01:30:30.000000+00', 'profile_pics/profile3.png', 'Theoretical physicist'),
('2024-06-21 01:40:40.000000+00', false, 'Isaac', 'Newton', false, '2024-06-21 01:40:40.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b775', 'isaacn', 'isaacnewton@gmail.com', 'gravity123', true, 'user', '2024-06-21 01:40:40.000000+00', '2024-06-21 01:40:40.000000+00', 'profile_pics/profile4.png', 'Mathematician and physicist'),
('2024-06-21 01:50:50.000000+00', false, 'Charles', 'Darwin', false, '2024-06-21 01:50:50.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b776', 'charlesd', 'charlesdarwin@gmail.com', 'evolution', true, 'user', '2024-06-21 01:50:50.000000+00', '2024-06-21 01:50:50.000000+00', 'profile_pics/profile5.png', 'Biologist and naturalist'),
('2024-06-21 02:00:00.000000+00', false, 'Nikola', 'Tesla', false, '2024-06-21 02:00:00.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b777', 'nikolat', 'nikolatesla@gmail.com', 'acdc123', true, 'user', '2024-06-21 02:00:00.000000+00', '2024-06-21 02:00:00.000000+00', 'profile_pics/profile6.png', 'Inventor and electrical engineer'),
('2024-06-21 02:10:10.000000+00', false, 'Leonardo', 'Da Vinci', false, '2024-06-21 02:10:10.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b778', 'leonardod', 'leonardodavinci@gmail.com', 'monalisa', true, 'user', '2024-06-21 02:10:10.000000+00', '2024-06-21 02:10:10.000000+00', 'profile_pics/profile7.png', 'Renaissance polymath'),
('2024-06-21 02:20:20.000000+00', false, 'Galileo', 'Galilei', false, '2024-06-21 02:20:20.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b779', 'galileog', 'galileogalilei@gmail.com', 'telescope', true, 'user', '2024-06-21 02:20:20.000000+00', '2024-06-21 02:20:20.000000+00', 'profile_pics/profile8.png', 'Astronomer and physicist'),
('2024-06-21 02:30:30.000000+00', false, 'Ada', 'Lovelace', false, '2024-06-21 02:30:30.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b780', 'adal', 'adalovelace@gmail.com', 'firstprogrammer', true, 'user', '2024-06-21 02:30:30.000000+00', '2024-06-21 02:30:30.000000+00', 'profile_pics/profile9.png', 'Mathematician and writer'),
('2024-06-21 02:40:40.000000+00', false, 'Thomas', 'Edison', false, '2024-06-21 02:40:40.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b781', 'thomase', 'thomasedison@gmail.com', 'lightbulb', true, 'user', '2024-06-21 02:40:40.000000+00', '2024-06-21 02:40:40.000000+00', 'profile_pics/profile10.png', 'Inventor and businessman'),
('2024-06-21 02:50:50.000000+00', false, 'Marie', 'Curie', false, '2024-06-21 02:50:50.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b782', 'mariec2', 'mariecurie2@gmail.com', 'radiation', true, 'user', '2024-06-21 02:50:50.000000+00', '2024-06-21 02:50:50.000000+00', 'profile_pics/profile11.png', 'Pioneer in radioactivity'),
('2024-06-21 03:00:00.000000+00', false, 'Rosalind', 'Franklin', false, '2024-06-21 03:00:00.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b783', 'rosalindf', 'rosalindfranklin@gmail.com', 'dna123', true, 'user', '2024-06-21 03:00:00.000000+00', '2024-06-21 03:00:00.000000+00', 'profile_pics/profile12.png', 'Chemist and X-ray crystallographer'),
('2024-06-21 03:10:10.000000+00', false, 'Alan', 'Turing', false, '2024-06-21 03:10:10.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b784', 'alant', 'alanturing@gmail.com', 'enigma', true, 'user', '2024-06-21 03:10:10.000000+00', '2024-06-21 03:10:10.000000+00', 'profile_pics/profile13.png', 'Mathematician and logician'),
('2024-06-21 03:20:20.000000+00', false, 'Grace', 'Hopper', false, '2024-06-21 03:20:20.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b785', 'graceh', 'gracehopper@gmail.com', 'cobol123', true, 'user', '2024-06-21 03:20:20.000000+00', '2024-06-21 03:20:20.000000+00', 'profile_pics/profile14.png', 'Computer scientist and naval officer'),
('2024-06-21 03:30:30.000000+00', false, 'Tim', 'Berners-Lee', false, '2024-06-21 03:30:30.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b786', 'timbl', 'timbernerslee@gmail.com', 'www123', true, 'user', '2024-06-21 03:30:30.000000+00', '2024-06-21 03:30:30.000000+00', 'profile_pics/profile15.png', 'Inventor of the World Wide Web'),
('2024-06-21 03:40:40.000000+00', false, 'Stephen', 'Hawking', false, '2024-06-21 03:40:40.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b787', 'stephenh', 'stephenhawking@gmail.com', 'blackholes', true, 'user', '2024-06-21 03:40:40.000000+00', '2024-06-21 03:40:40.000000+00', 'profile_pics/profile16.png', 'Theoretical physicist and cosmologist'),
('2024-06-21 03:50:50.000000+00', false, 'Katherine', 'Johnson', false, '2024-06-21 03:50:50.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b788', 'katherinej', 'katherinejohnson@gmail.com', 'nasa123', true, 'user', '2024-06-21 03:50:50.000000+00', '2024-06-21 03:50:50.000000+00', 'profile_pics/profile17.png', 'Mathematician and space scientist'),
('2024-06-21 04:00:00.000000+00', false, 'Mae', 'Jemison', false, '2024-06-21 04:00:00.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b789', 'maej', 'maejemison@gmail.com', 'space123', true, 'user', '2024-06-21 04:00:00.000000+00', '2024-06-21 04:00:00.000000+00', 'profile_pics/profile18.png', 'Engineer, physician, and astronaut'),
('2024-06-21 04:10:10.000000+00', false, 'Neil', 'Armstrong', false, '2024-06-21 04:10:10.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b790', 'neila', 'neilarmstrong@gmail.com', 'moonwalker', true, 'user', '2024-06-21 04:10:10.000000+00', '2024-06-21 04:10:10.000000+00', 'profile_pics/profile19.png', 'First person to walk on the Moon'),
('2024-06-21 04:20:20.000000+00', false, 'Elon', 'Musk', false, '2024-06-21 04:20:20.000000+00', '9d4e2f08-009e-41a8-94a2-9fd91a68b791', 'elonm', 'elonmusk@gmail.com', 'tesla123', true, 'user', '2024-06-21 04:20:20.000000+00', '2024-06-21 04:20:20.000000+00', 'profile_pics/profile20.png', 'Entrepreneur and business magnate');
