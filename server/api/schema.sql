DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS setting_control_types;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS logs;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  pwd TEXT NOT NULL
);
CREATE TABLE setting_control_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL
);

CREATE TABLE dectector(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, icon TEXT);

CREATE TABLE setting_category(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
icon TEXT NULL,
route TEXT NULL,
parent INTEGER NOT NULL DEFAULT 0);

CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL DEFAULT '',
    setting_category_id INTEGER NOT NULL,
    setting_detector_id INTEGER NULL,
    setting_control_type_id INTEGER NOT NULL DEFAULT 1,
    setting_required BIT NULL,
    setting_placeholder TEXT NULL,
    setting_label TEXT NULL,
    setting_help TEXT NULL,
    sort_order INTEGER NOT NULL,
    max_value TEXT NULL,
    min_value TEXT NULL,
    step TEXT NULL,
    FOREIGN KEY(setting_control_type_id) REFERENCES setting_control_types(id),
    FOREIGN KEY(setting_category_id) REFERENCES setting_category(id)
);

CREATE TABLE video(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_url TEXT NOT NULL,
    video_input_mode TEXT NOT NULL
);

CREATE TABLE statuses(id INTEGER PRIMARY KEY AUTOINCREMENT, status_name TEXT NOT NULL, status_value TEXT NOT NULL, status_display TEXT NOT NULL, sort_order INT NOT NULL);

CREATE TABLE logs(id INTEGER PRIMARY KEY AUTOINCREMENT, submitted_date DATETIME NOT NULL, log_message TEXT NOT NULL);

INSERT INTO setting_control_types(kind) VALUES('tb'), ('checkbox'), ('ddl'), ('number'),('decflt'), ('pwd');

INSERT INTO setting_category(name, icon, route) VALUES ('MXSERVER', 'fa fa-server fa-x3', '/settings/mxserver'),
                                          ('Video Source', 'fa fa-video-camera fa-x3', '/settings/video'),
                                          ('Network Configuration', 'fa fa-share-alt fa-x3', '/settings/network'),
                                          ('Set Detection', 'fa fa-cogs fa-x3', '/settings/detection');
INSERT INTO detector(name, icon) VALUES('Faces', 'fa fa-user fa-x3'),('Objects', 'fa fa-cubes fa-x3')
INSERT INTO setting_category(name, parent)
VALUES ('Face', (SELECT id FROM setting_category WHERE name = 'Search Settings')),
       ('Vehicles', (SELECT id FROM setting_category WHERE name = 'Search Settings')),
       ('Weapons', (SELECT id FROM setting_category WHERE name = 'Search Settings'));

INSERT INTO settings(setting_name, setting_value, setting_category_id, setting_control_type_id, setting_label, setting_help, setting_required, setting_placeholder, sort_order, min_value, max_value, step)
VALUES('mx-host', 'myserver.mxservercloud.com', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1),'MXSERVER Host Name', 'Enter the name of the server hosting MXSERVER application', 1, 'localhost', 1, NULL, NULL, NULL),
('mx-username', 'User', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'MXSERVER Username', 'Enter the name to use when logging into MXSERVER', 1, 'user',2, NULL, NULL, NULL),
('mx-pass', 'Password', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'pwd' LIMIT 1),'MXSERVER Password', 'Enter the password to use when connecting to MXSERVER', 1, NULL,3, NULL, NULL, NULL),
('mx-use-tls', 'True', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Use TLS', 'Enable when connecting to a secure website (https)', 0, NULL,4, NULL, NULL, NULL),
('mx-use-offlinemode', 'False', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Use Offline Mode', 'Save images to local disk, which can be downloaded.', 0, NULL, 25, NULL, NULL, NULL),
('bypass-cert-validation', 'False', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Bypass Certificate Validation','Enable when using a self signed certificate', 0, NULL, 5, NULL, NULL, NULL),
('rtsp-url', 'rtsp://root:secret@192.168.1.120/axis-media/media.3gp', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'Video URL', 'Default RTSP stream URL', 0, NULL, 6, NULL, NULL, NULL),
('conn-type', '2', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'ddl' LIMIT 1), 'Connection Type', 'Select connection type', 0, 'rtps',7, NULL, NULL, NULL),
('auto-restart-stream', 'False', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Auto restart stream', 'Reconnect to video stream if server restarts', 0, NULL,9, NULL, NULL, NULL),
('resize-image-before-prediction', 'False', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Resize Image Before Processing', 'Reduce frame resolution to speed processing', 0, NULL,9, NULL, NULL, NULL),
('resize-image-width', '800', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1),'Resize Image Width', 'Enter desired image width', 0, '800',10, NULL, NULL, '1'),
('detection-thrshl', '0.8', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'decflt' LIMIT 1), 'Face Detection Threshold', 'Mininum face quality to begin detecting faces (0-1)', 1, '0.1',11, '0', '1', '0.01'),
('min-face-size', '4', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1),'Min Face Size', 'Minimum face size to detect as a percentage of frame resolution', 1, '4',12, '0', '100', '1'),
('min-face-qual-score', '9', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'decflt' LIMIT 1), 'Face Submission Threshold', 'Minimum face quality required for face to be submitted for matching (0 - 10)', 1, '1.0',13, '0', '10', '0.01'),
('max-faces-to-submit-while-tracking', '3', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1), 'Max Faces to Submit While Tracking', 'The max number of faces that will be submitted for matching from a single track', 1, '3',14, NULL, NULL, NULL),
('max-objects-to-detect', '50', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1), 'Max Faces to Detect', 'The maximum number of fraces to detect & track in a single frame', 1, '50',15, NULL, NULL, NULL),
('tracking-max-age', '1', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1), 'Face Track Timeout', 'Number of seconds face is not present in track before track termination', 1, '1',16, NULL, NULL, NULL),
('tracking-min-hits', '3', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'number' LIMIT 1), 'Min Frames Face Detected', 'Minimum number of frames a face must be detected before tracking begins', 1, '3', 17, NULL, NULL, NULL),
('tracking-min-iou', '0.6', (SELECT id FROM setting_category WHERE name = 'Video Source'), (SELECT id FROM setting_control_types WHERE kind = 'decflt' LIMIT 1), 'Detect Overlapping Faces', 'Percentage of overlap to correlate detected and tracked faces', 0, '0.6',18, NULL, NULL, NULL),
('mx-search-path', '/api/face-searches', (SELECT id FROM setting_category WHERE name = 'MXSERVER'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'MXSERVER API URL', 'API method to use for search submission', 1, '/api/face-searches',20, NULL, NULL, NULL),
('mx-retain-image', 'False', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Retain Image', 'Retain search image in photo repository', 0, NULL,22, NULL, NULL, NULL),
('mx-media-search', 'False', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Media Search', 'Search video/photo repository in addition to watchlists', 0, NULL,23, NULL, NULL, NULL),
('mx-collected-from', 'MatchBox Edge', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'Device Name', 'Enter device name', 1, 'Matchbox Edge',24, NULL, NULL, NULL),
('mx-collected-location', 'Default', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'Device Location', 'Enter location of the device', 0, 'Bldg',25, NULL, NULL, NULL),
('mx-watchlists', ' ', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'tb' LIMIT 1), 'Watchlists', 'Enter comma seperated list of MXSERVER watchlist IDs', 0, NULL,26, NULL, NULL, NULL),
('should-submit-face-searches', 'True', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Submit Face Searches', 'Submit faces to MXSERVER for searching', 0, NULL,21, NULL, NULL, NULL),
('face-cache-processing-interval', '1.0', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'decflt' LIMIT 1), 'Face Search Submission Interval', 'Enter number of seconds to delay submission of subsequent face searches', 1, '1.0', 29, NULL, NULL, NULL),
('print-scores-ids-on-submit-images', 'False', (SELECT id FROM setting_category WHERE name = 'Face'), (SELECT id FROM setting_control_types WHERE kind = 'checkbox' LIMIT 1), 'Add Quality Scores and IDs to Submitted Images', 'Display face quality score and track ID to extracted face image', 0, NULL,30, NULL, NULL, NULL);

INSERT INTO statuses(status_name, status_value, status_display, sort_order)
VALUES('StatusType.SERVER', 'False', 'MXSERVER Connection', 1),
('StatusType.STREAM', 'False', 'Video Stream', 5),
('StatusType.FACEFIND', 'False', 'Face Detection', 10),
('StatusType.SEARCH', 'False', 'Face Search Submission', 15);
