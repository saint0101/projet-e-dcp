-- -------------------------------------------------------------
-- TablePlus 6.1.2(568)
--
-- https://tableplus.com/
--
-- Database: edcp_db
-- Generation Time: 2024-08-29 08:21:55.0610
-- -------------------------------------------------------------


INSERT INTO "public"."auth_group" ("id", "name") VALUES
(1, 'Validateurs_niv_1'),
(2, 'Validateurs_niv_2'),
(3, 'Validateurs_niv_3'),
(4, 'Validateurs_niv_4'),
(5, 'Validateurs_niv_5'),
(6, 'Agents') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."auth_group_permissions" ("id", "group_id", "permission_id") VALUES
(1, 1, 153),
(2, 2, 154),
(3, 4, 156),
(4, 5, 157),
(5, 3, 155),
(6, 6, 65),
(7, 6, 66),
(8, 6, 67),
(9, 6, 68) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."auth_permission" ("id", "name", "content_type_id", "codename") VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Utilisateur', 6, 'add_user'),
(22, 'Can change Utilisateur', 6, 'change_user'),
(23, 'Can delete Utilisateur', 6, 'delete_user'),
(24, 'Can view Utilisateur', 6, 'view_user'),
(25, 'Can add role', 7, 'add_role'),
(26, 'Can change role', 7, 'change_role'),
(27, 'Can delete role', 7, 'delete_role'),
(28, 'Can view role', 7, 'view_role'),
(29, 'Can add notification', 8, 'add_notification'),
(30, 'Can change notification', 8, 'change_notification'),
(31, 'Can delete notification', 8, 'delete_notification'),
(32, 'Can view notification', 8, 'view_notification'),
(33, 'Can add Journal Transaction', 9, 'add_journaltransaction'),
(34, 'Can change Journal Transaction', 9, 'change_journaltransaction'),
(35, 'Can delete Journal Transaction', 9, 'delete_journaltransaction'),
(36, 'Can view Journal Transaction', 9, 'view_journaltransaction'),
(37, 'Can add group extension', 10, 'add_groupextension'),
(38, 'Can change group extension', 10, 'change_groupextension'),
(39, 'Can delete group extension', 10, 'delete_groupextension'),
(40, 'Can view group extension', 10, 'view_groupextension'),
(41, 'Can add Enregistrement', 11, 'add_enregistrement'),
(42, 'Can change Enregistrement', 11, 'change_enregistrement'),
(43, 'Can delete Enregistrement', 11, 'delete_enregistrement'),
(44, 'Can view Enregistrement', 11, 'view_enregistrement'),
(45, 'Can add Nom de groupe d'utilisateurs', 12, 'add_groupname'),
(46, 'Can change Nom de groupe d'utilisateurs', 12, 'change_groupname'),
(47, 'Can delete Nom de groupe d'utilisateurs', 12, 'delete_groupname'),
(48, 'Can view Nom de groupe d'utilisateurs', 12, 'view_groupname'),
(49, 'Can add Pays', 13, 'add_pays'),
(50, 'Can change Pays', 13, 'change_pays'),
(51, 'Can delete Pays', 13, 'delete_pays'),
(52, 'Can view Pays', 13, 'view_pays'),
(53, 'Can add secteur', 14, 'add_secteur'),
(54, 'Can change secteur', 14, 'change_secteur'),
(55, 'Can delete secteur', 14, 'delete_secteur'),
(56, 'Can view secteur', 14, 'view_secteur'),
(57, 'Can add Statut de demande ou d'analyse', 15, 'add_status'),
(58, 'Can change Statut de demande ou d'analyse', 15, 'change_status'),
(59, 'Can delete Statut de demande ou d'analyse', 15, 'delete_status'),
(60, 'Can view Statut de demande ou d'analyse', 15, 'view_status'),
(61, 'Can add Type Client', 16, 'add_typeclient'),
(62, 'Can change Type Client', 16, 'change_typeclient'),
(63, 'Can delete Type Client', 16, 'delete_typeclient'),
(64, 'Can view Type Client', 16, 'view_typeclient'),
(65, 'Can add Type de pièce', 17, 'add_typepiece'),
(66, 'Can change Type de pièce', 17, 'change_typepiece'),
(67, 'Can delete Type de pièce', 17, 'delete_typepiece'),
(68, 'Can view Type de pièce', 17, 'view_typepiece'),
(69, 'Can add Action effectuée', 18, 'add_actiondemande'),
(70, 'Can change Action effectuée', 18, 'change_actiondemande'),
(71, 'Can delete Action effectuée', 18, 'delete_actiondemande'),
(72, 'Can view Action effectuée', 18, 'view_actiondemande'),
(73, 'Can add Analyse d'une demande', 19, 'add_analysedemande'),
(74, 'Can change Analyse d'une demande', 19, 'change_analysedemande'),
(75, 'Can delete Analyse d'une demande', 19, 'delete_analysedemande'),
(76, 'Can view Analyse d'une demande', 19, 'view_analysedemande'),
(77, 'Peut valider la demande - niveau 1', 19, 'can_validate_niv_1'),
(78, 'Peut valider la demande - niveau 2', 19, 'can_validate_niv_2'),
(79, 'Peut valider la demande - niveau 3', 19, 'can_validate_niv_3'),
(80, 'Peut valider la demande - niveau 4', 19, 'can_validate_niv_4'),
(81, 'Peut valider la demande - niveau 5', 19, 'can_validate_niv_5'),
(82, 'Can add Categorie de demande', 20, 'add_categoriedemande'),
(83, 'Can change Categorie de demande', 20, 'change_categoriedemande'),
(84, 'Can delete Categorie de demande', 20, 'delete_categoriedemande'),
(85, 'Can view Categorie de demande', 20, 'view_categoriedemande'),
(86, 'Can add Demande', 21, 'add_demande'),
(87, 'Can change Demande', 21, 'change_demande'),
(88, 'Can delete Demande', 21, 'delete_demande'),
(89, 'Can view Demande', 21, 'view_demande'),
(90, 'Can add Type de réponse', 22, 'add_typereponse'),
(91, 'Can change Type de réponse', 22, 'change_typereponse'),
(92, 'Can delete Type de réponse', 22, 'delete_typereponse'),
(93, 'Can view Type de réponse', 22, 'view_typereponse'),
(94, 'Can add validation demande', 23, 'add_validationdemande'),
(95, 'Can change validation demande', 23, 'change_validationdemande'),
(96, 'Can delete validation demande', 23, 'delete_validationdemande'),
(97, 'Can view validation demande', 23, 'view_validationdemande'),
(98, 'Can add reponse demande', 24, 'add_reponsedemande'),
(99, 'Can change reponse demande', 24, 'change_reponsedemande'),
(100, 'Can delete reponse demande', 24, 'delete_reponsedemande'),
(101, 'Can view reponse demande', 24, 'view_reponsedemande'),
(102, 'Can add Historique de la demande', 25, 'add_historiquedemande'),
(103, 'Can change Historique de la demande', 25, 'change_historiquedemande'),
(104, 'Can delete Historique de la demande', 25, 'delete_historiquedemande'),
(105, 'Can view Historique de la demande', 25, 'view_historiquedemande'),
(106, 'Can add critere evaluation', 26, 'add_critereevaluation'),
(107, 'Can change critere evaluation', 26, 'change_critereevaluation'),
(108, 'Can delete critere evaluation', 26, 'delete_critereevaluation'),
(109, 'Can view critere evaluation', 26, 'view_critereevaluation'),
(110, 'Can add Commentaire sur une demande', 27, 'add_commentaire'),
(111, 'Can change Commentaire sur une demande', 27, 'change_commentaire'),
(112, 'Can delete Commentaire sur une demande', 27, 'delete_commentaire'),
(113, 'Can view Commentaire sur une demande', 27, 'view_commentaire'),
(114, 'Can add Agrement DCP', 28, 'add_agrementdcp'),
(115, 'Can change Agrement DCP', 28, 'change_agrementdcp'),
(116, 'Can delete Agrement DCP', 28, 'delete_agrementdcp'),
(117, 'Can view Agrement DCP', 28, 'view_agrementdcp'),
(118, 'Can add Correspondant personne morale', 29, 'add_cabinetdpo'),
(119, 'Can change Correspondant personne morale', 29, 'change_cabinetdpo'),
(120, 'Can delete Correspondant personne morale', 29, 'delete_cabinetdpo'),
(121, 'Can view Correspondant personne morale', 29, 'view_cabinetdpo'),
(122, 'Can add Mode d'exercice de l'activité', 30, 'add_exerciceactivite'),
(123, 'Can change Mode d'exercice de l'activité', 30, 'change_exerciceactivite'),
(124, 'Can delete Mode d'exercice de l'activité', 30, 'delete_exerciceactivite'),
(125, 'Can view Mode d'exercice de l'activité', 30, 'view_exerciceactivite'),
(126, 'Can add Moyens du DPO', 31, 'add_moyensdpo'),
(127, 'Can change Moyens du DPO', 31, 'change_moyensdpo'),
(128, 'Can delete Moyens du DPO', 31, 'delete_moyensdpo'),
(129, 'Can view Moyens du DPO', 31, 'view_moyensdpo'),
(130, 'Can add Qualifications du Correspondant', 32, 'add_qualificationsdpo'),
(131, 'Can change Qualifications du Correspondant', 32, 'change_qualificationsdpo'),
(132, 'Can delete Qualifications du Correspondant', 32, 'delete_qualificationsdpo'),
(133, 'Can view Qualifications du Correspondant', 32, 'view_qualificationsdpo'),
(134, 'Can add Type de Correspondant', 33, 'add_typedpo'),
(135, 'Can change Type de Correspondant', 33, 'change_typedpo'),
(136, 'Can delete Type de Correspondant', 33, 'delete_typedpo'),
(137, 'Can view Type de Correspondant', 33, 'view_typedpo'),
(138, 'Can add Désignation de DPO personne morale', 34, 'add_designationdpomoral'),
(139, 'Can change Désignation de DPO personne morale', 34, 'change_designationdpomoral'),
(140, 'Can delete Désignation de DPO personne morale', 34, 'delete_designationdpomoral'),
(141, 'Can view Désignation de DPO personne morale', 34, 'view_designationdpomoral'),
(142, 'Can add Correspondant à la protection des données', 35, 'add_correspondant'),
(143, 'Can change Correspondant à la protection des données', 35, 'change_correspondant'),
(144, 'Can delete Correspondant à la protection des données', 35, 'delete_correspondant'),
(145, 'Can view Correspondant à la protection des données', 35, 'view_correspondant'),
(146, 'Can add Demande d'autorisation', 36, 'add_demandeauto'),
(147, 'Can change Demande d'autorisation', 36, 'change_demandeauto'),
(148, 'Can delete Demande d'autorisation', 36, 'delete_demandeauto'),
(149, 'Can view Demande d'autorisation', 36, 'view_demandeauto'),
(150, 'Can add Echelle de notation', 37, 'add_echellenotation'),
(151, 'Can change Echelle de notation', 37, 'change_echellenotation'),
(152, 'Can delete Echelle de notation', 37, 'delete_echellenotation'),
(153, 'Can view Echelle de notation', 37, 'view_echellenotation'),
(154, 'Can add finalite', 38, 'add_finalite'),
(155, 'Can change finalite', 38, 'change_finalite'),
(156, 'Can delete finalite', 38, 'delete_finalite'),
(157, 'Can view finalite', 38, 'view_finalite'),
(158, 'Can add Catégorie de personnes concernées', 39, 'add_persconcernee'),
(159, 'Can change Catégorie de personnes concernées', 39, 'change_persconcernee'),
(160, 'Can delete Catégorie de personnes concernées', 39, 'delete_persconcernee'),
(161, 'Can view Catégorie de personnes concernées', 39, 'view_persconcernee'),
(162, 'Can add demande auto biometrie', 40, 'add_demandeautobiometrie'),
(163, 'Can change demande auto biometrie', 40, 'change_demandeautobiometrie'),
(164, 'Can delete demande auto biometrie', 40, 'delete_demandeautobiometrie'),
(165, 'Can view demande auto biometrie', 40, 'view_demandeautobiometrie'),
(166, 'Can add demande auto traitement', 41, 'add_demandeautotraitement'),
(167, 'Can change demande auto traitement', 41, 'change_demandeautotraitement'),
(168, 'Can delete demande auto traitement', 41, 'delete_demandeautotraitement'),
(169, 'Can view demande auto traitement', 41, 'view_demandeautotraitement'),
(170, 'Can add demande auto transfert', 42, 'add_demandeautotransfert'),
(171, 'Can change demande auto transfert', 42, 'change_demandeautotransfert'),
(172, 'Can delete demande auto transfert', 42, 'delete_demandeautotransfert'),
(173, 'Can view demande auto transfert', 42, 'view_demandeautotransfert'),
(174, 'Can add demande auto video', 43, 'add_demandeautovideo'),
(175, 'Can change demande auto video', 43, 'change_demandeautovideo'),
(176, 'Can delete demande auto video', 43, 'delete_demandeautovideo'),
(177, 'Can view demande auto video', 43, 'view_demandeautovideo'),
(178, 'Can add Type de demande', 44, 'add_typedemandeauto'),
(179, 'Can change Type de demande', 44, 'change_typedemandeauto'),
(180, 'Can delete Type de demande', 44, 'delete_typedemandeauto'),
(181, 'Can view Type de demande', 44, 'view_typedemandeauto'),
(182, 'Can add sous finalite', 45, 'add_sousfinalite'),
(183, 'Can change sous finalite', 45, 'change_sousfinalite'),
(184, 'Can delete sous finalite', 45, 'delete_sousfinalite'),
(185, 'Can view sous finalite', 45, 'view_sousfinalite') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."base_edcp_enregistrement" ("id", "created_at", "raisonsociale", "idu", "representant", "rccm", "telephone", "email_contact", "site_web", "ville", "adresse_geo", "adresse_bp", "gmaps_link", "effectif", "presentation", "num_piece", "has_dpo", "file_piece", "file_rccm", "file_mandat", "pays_id", "secteur_id", "type_piece_id", "typeclient_id", "user_id") VALUES
(3, '2024-08-28 20:08:50.722838+00', 'JOJO SARLU', '0000309132', 'JOJO Charles', '22223', '9320230923', 'mail@mail.com', 'http://www.mail.com', 'Abidjan', 'adresse adresse', NULL, NULL, 1, ', NULL, 'f', ', ', ', 1, 2, 1, 1, 3),
(4, '2024-08-28 20:10:10.216079+00', 'PME1', '390092092', 'JOJO Charlotte', '33334', '299022', 'mail@mail.com', NULL, 'Paris', 'Cachan', NULL, NULL, 39, ', NULL, 'f', ', 'docs/enregistrement/guide_utilisation_baobab_OK.pdf', ', 3, 3, NULL, 2, 3),
(5, '2024-08-28 20:25:10.990787+00', 'SuperDPO SARL', '099009', ', '5555', '32329239823', 'mail@mail.com', NULL, 'Abidjan', NULL, NULL, NULL, NULL, ', NULL, 'f', ', ', ', 1, 4, NULL, 2, 6),
(6, '2024-08-28 20:25:48.987419+00', 'Best DPO SA', '67562', 'James Miller', NULL, '0576950214', 'millenium.walka@yahoo.com', NULL, 'Accra', 'Cachan', '94230', NULL, NULL, ', NULL, 'f', ', ', ', 4, NULL, NULL, 3, 7),
(7, '2024-08-28 20:27:27.888443+00', 'ADM', 'I2222', 'BOBO Jacob', '0777', '920209202', 'mail@mail.com', NULL, 'Bouaké', NULL, NULL, NULL, 300, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', NULL, 'f', ', 'docs/enregistrement/ticket.pdf', ', 1, 3, NULL, 4, 3) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."base_edcp_groupextension" ("id", "niv_validation", "group_id", "group_name_id") VALUES
(2, 1, 1, 2),
(3, 2, 2, 3),
(4, 3, 3, 4),
(5, 4, 4, 5),
(6, 5, 5, 6),
(7, 0, 6, 1) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."base_edcp_user" ("id", "password", "last_login", "is_superuser", "email", "created_at", "username", "avatar", "nom", "prenoms", "organisation", "telephone", "fonction", "is_active", "is_staff", "email_verified", "must_reset", "is_dpo", "is_business_account", "consentement") VALUES
(1, 'pbkdf2_sha256$600000$8tLOkvZo6iWEK1k2KBTSpA$2HEpTr5ObvdQYSf+i9UWJKcZ3M9tXvLjr7ZBq+C5pcU=', '2024-08-28 20:17:40.16209+00', 't', 'admin@mail.com', '2024-08-28 18:48:25.607146+00', 'admin', ', 'admin', 'admin', NULL, NULL, NULL, 't', 't', 'f', 'f', 'f', 'f', 'f'),
(2, 'pbkdf2_sha256$600000$gUfpXrOZhUxYZRz3mX84Fd$D6BUPeXwiTebvvMTb6aY0G74nGjkCnkoML1HLUM0Y4w=', NULL, 'f', 'mail02@mail.com', '2024-08-28 19:15:52.688976+00', ', ', 'POI', 'kjzjzekj', 'LKZLKZl', '2P32P23', ', 'f', 'f', 'f', 'f', 'f', 'f', 't'),
(3, 'pbkdf2_sha256$600000$pwUpi2TVShEuoYBdOCjC4b$gesVWpXWP9yV11+sP6s3gr+f8h5HyrQWx/h9uHJvJdE=', '2024-08-28 20:14:56.341079+00', 'f', 'client1@mail.com', '2024-08-28 19:51:38.97224+00', ', ', 'JOJO', 'Charles', 'PME1', '0102030405', 'Manager', 't', 'f', 't', 'f', 'f', 'f', 't'),
(4, 'pbkdf2_sha256$600000$UVM7fv4OSjJXGjITSrL1YJ$Inc85b++S3gVUYi1K666MGqS8OA9DGHWnODdyvps25M=', NULL, 'f', 'client2@mail.com', '2024-08-28 19:53:01.189379+00', ', ', 'COCO', 'Simon', 'Super Bank', '01003040505', 'CEO', 't', 'f', 't', 'f', 'f', 'f', 't'),
(5, 'pbkdf2_sha256$600000$knbhyfBqRGHEdsoWQIQA4b$L9Gs2mrqz6r5lvt2CohXMOQMkGH2UxWulMYs9n6/UqI=', NULL, 'f', 'client3@mail.com', '2024-08-28 19:54:12.822456+00', ', ', 'TOTO', 'Carlos', 'MPP', '09989887', NULL, 't', 'f', 't', 'f', 'f', 'f', 't'),
(6, 'pbkdf2_sha256$600000$L8gxgZxUq92ekE4VDlUXiH$s62dpYRfIqgCZZ2DH0ot5Xtryr6XPQDWgq0dyK6NF9s=', NULL, 'f', 'dpo1@mail.com', '2024-08-28 19:57:14.965721+00', ', ', 'DPO1', 'DPO1', 'Super DPO', '82872872738', NULL, 't', 'f', 't', 'f', 'f', 't', 't'),
(7, 'pbkdf2_sha256$600000$SXJydS5U03m0aWDB6rwTuS$srb0GdxVgKPrm1Z46gEEX8GMRDOUUxmXNyud4grf0Ms=', NULL, 'f', 'dpo2@mail.com', '2024-08-28 19:58:15.932098+00', ', ', 'DPO2', 'DPO2', 'Best DPO', '9229298', 'Agent', 't', 'f', 't', 'f', 'f', 't', 't'),
(8, 'pbkdf2_sha256$600000$q2qMuM4oEyjV124h086tCg$iBk4bkoqY4DDjEP8cfoFNepcAlcdJ5Yj3m+pHpCdCbQ=', '2024-08-28 20:28:35.118944+00', 'f', 'agent1@mail.com', '2024-08-28 19:59:28.69361+00', ', ', 'Agent', 'No1', 'ARTCI', NULL, NULL, 't', 't', 't', 'f', 'f', 'f', 't'),
(9, 'pbkdf2_sha256$600000$mcYwf8zsnDEMFptU2cMQpO$MOilOfSD0y9rEYVPkRYKrmgzaVbrkW1uEatxRQiExd8=', '2024-08-28 20:30:25.347575+00', 'f', 'superviseur1@mail.com', '2024-08-28 20:00:30.22748+00', ', ', 'Superv', 'No1', 'ARTCI', '090090', 'CS', 't', 't', 't', 'f', 'f', 'f', 't'),
(10, 'pbkdf2_sha256$600000$u5XNCJykEilYIr9SXluSDw$++1DJJUsx0bqbRkX6Kflr75qrqWAJ2CnZPRT3dXYkzY=', '2024-08-28 20:30:55.372514+00', 'f', 'manager1@mail.com', '2024-08-28 20:01:22.323481+00', ', ', 'Manager', 'No1', 'ARTCI', '00101', 'Manager', 't', 't', 't', 'f', 'f', 'f', 't'),
(11, 'pbkdf2_sha256$600000$jrCKkrYfJYwiZmpJoj2nu5$WrFk4g6ASNbIrCFk4wW/vJ0PYUKKSzchWjkxvcnD81U=', '2024-08-28 20:31:20.959599+00', 'f', 'directeur@mail.com', '2024-08-28 20:02:14.721756+00', ', ', 'Directeur', 'Dir', 'ARTCI', '023099032', 'Directeur', 't', 't', 't', 'f', 'f', 'f', 't'),
(12, 'pbkdf2_sha256$600000$kJFMrXvS3LQAuVPXaR1nxQ$NjR8LpMZrYnqu10Nh+cozeuLQe+iUNK0z0U286T3kzM=', NULL, 'f', 'dg@mail.com', '2024-08-28 20:03:04.247999+00', ', ', 'Directeur', 'Général', 'ARTCI', '0900090', 'DG', 't', 't', 't', 'f', 'f', 'f', 't'),
(13, 'pbkdf2_sha256$600000$vnrmxq6AkLPvmENkWz06to$JS3mbNtmO0fLlLiWeiYgLeJ4qnrBuzgbO+MbqrsxJMY=', NULL, 'f', 'pcr@mail.com', '2024-08-28 20:03:43.925093+00', ', ', 'PCR', 'PCR', 'ARTCI', '02039023', 'PCR', 't', 't', 't', 'f', 'f', 'f', 't') ON CONFLICT (id) DO UPDATE SET column1 = EXCLUDED.column1, column2 = EXCLUDED.column2;

INSERT INTO "public"."base_edcp_user_groups" ("id", "user_id", "group_id") VALUES
(1, 8, 6),
(2, 9, 1),
(3, 10, 2),
(4, 11, 3),
(5, 12, 4),
(6, 13, 5) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_cabinetdpo" ("enregistrement_ptr_id") VALUES
(5),
(6) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_correspondant" ("demande_ptr_id", "is_personne_morale", "experiences", "profile_completed", "is_active", "is_approved", "is_rejected", "commentaires", "file_lettre_designation", "file_lettre_acceptation", "file_attestation_travail", "file_casier_judiciaire", "file_certificat_nationalite", "file_cv", "file_contrat", "cabinet_id", "exercice_activite_id", "qualifications_id", "type_dpo_id", "user_id") VALUES
(1, 'f', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 't', 't', 'f', 'f', NULL, 'docs/correspondant/signature.png', 'docs/correspondant/guide_utilisation_baobab_OK.pdf', ', ', ', ', ', NULL, 1, 1, 1, 3),
(2, 't', NULL, 'f', 't', 'f', 'f', ', ', ', ', ', ', ', 'docs/correspondant/signature_bH44G24.png', 5, NULL, NULL, 2, 6) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_correspondant_moyens_dpo" ("id", "correspondant_id", "moyensdpo_id") VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_exerciceactivite" ("id", "label", "description") VALUES
(1, 'Temps plein', '),
(2, 'Temps partiel', ') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_moyensdpo" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'personnel', 'f', 'Affectation de personnel', ', 1),
(2, 'budget', 'f', 'Budget spécifique', ', 2),
(3, 'formations', 'f', 'Formations', ', 3),
(4, 'accompagnement', 'f', 'Accompagnement technique et juridique', ', 5) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_qualificationsdpo" ("id", "label", "description") VALUES
(1, 'Informatique', '),
(2, 'Sciences Juridiques', '),
(4, 'Réseaux et télécommunication', '),
(5, 'Qualité / conformité', ') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."correspondant_typedpo" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'personne_physique', 'f', 'Personne physique', ', 0),
(2, 'personne_morale', 'f', 'Personne morale', ', 1) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_actiondemande" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'creation', 'f', 'Création', NULL, 0),
(2, 'mise_a_jour', 'f', 'Mise à jour', NULL, 0),
(3, 'commentaires', 'f', 'Commentaires', ', 0),
(4, 'changement_statut', 'f', 'Changement de statut', ', 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_analysedemande" ("id", "created_at", "updated_at", "evaluation", "observations", "prescriptions", "avis_juridique", "avis_technique", "niv_validation", "is_locked", "is_closed", "created_by_id", "projet_reponse_id", "status_id", "updated_by_id", "validation_niv1_id", "validation_niv2_id", "validation_niv3_id", "validation_niv4_id", "validation_niv5_id") VALUES
(1, '2024-08-28 20:28:48.136789+00', '2024-08-28 20:29:10.006958+00', '{"dossier_complet": "2", "profil": "1"}', 'Blabla', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 't', 'f', 3, 't', 't', 8, 1, 11, 8, NULL, NULL, NULL, NULL, NULL) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_analysedemande_validations" ("id", "analysedemande_id", "validationdemande_id") VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_echellenotation" ("id", "label", "is_sensible", "description", "resume", "ordre", "valeur") VALUES
(1, 'ok', 'f', 'Satisfaisant', ', 0, 10),
(2, 'partiel', 'f', 'Partiellement satisfaisant', ', 0, 5),
(3, 'not_ok', 'f', 'Non satisfaisant', ', 0, 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_finalite" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'ressources_humaines', 'f', 'Gestion des ressources humaines', ', 1),
(2, 'paie', 'f', 'Gestion de la paie', ', 2),
(3, 'recrutement', 'f', 'Gestion du recrutement', ', 3),
(4, 'clientele', 'f', 'Gestion de la clientèle', ', 4),
(5, 'videosurveillance', 'f', 'Gestion de la vidéosurveillance', ', 5),
(6, 'biometrie', 'f', 'Gestion de la biométrie', ', 7),
(7, 'transferts', 'f', 'Transferts de données', ', 8) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_persconcernee" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'salaries', 'f', 'Salariés', ', 1),
(2, 'clients', 'f', 'Clients', ', 2),
(3, 'visiteurs', 'f', 'Visiteurs', ', 3),
(4, 'enfants', 'f', 'Enfants', ', 4) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_sousfinalite" ("id", "label", "is_sensible", "description", "resume", "ordre", "finalite_id") VALUES
(1, 'declaration_cnps', 'f', 'Déclaration des salariés auprès de la CNPS/CGRAE', ', 1, 1),
(2, 'obligations_sociales', 'f', 'Respect des obligations en matière sociales', ', 2, 1),
(3, 'retraite', 'f', 'Paiement des droits de départs à la retraite', ', 3, 1),
(4, 'remuneration', 'f', 'Calcul des rémunérations', ', 1, 2),
(5, 'virement', 'f', 'Ordre de virement à la banque', ', 3, 2),
(6, 'appel_candidature', 'f', 'Appel à candidature en vue du recrutement', ', 1, 3),
(7, 'entretien', 'f', 'Entretien d’embauche', ', 2, 3),
(8, 'compte', 'f', 'Ouverture de compte', ', 1, 4),
(9, 'experience_client', 'f', 'Gestion de l'expérience client', ', 2, 4),
(10, 'securite', 'f', 'Sécurité des biens et des personnes', ', 1, 5),
(11, 'controle', 'f', 'Contrôle de présence des salariés', ', 2, 5),
(12, 'controle_acces', 't', 'Contrôle d’accès aux zones sensibles', ', 1, 6),
(14, 'securite_donnees', 't', 'Sécurité des données', ', 0, 6),
(15, 'hebergement', 'f', 'Hébergement des données', ', 1, 7),
(16, 'communication', 'f', 'Communication des données à la maison mère', ', 2, 7) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_typedemandeauto" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'traitement', 'f', 'Traitement de données à caractère personnel', 'Traitement de données à caractère personnel : exemples de finalités, cas d'usage etc. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi', 1),
(2, 'transfert', 'f', 'Transfert de données à caractère personnel', 'Transfert de données à caractère personnel : exemples de finalités, cas d'usage etc. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi', 2),
(3, 'videosurveillance', 'f', 'Installation de dispositif de vidéosurveillance', 'Dispositifs de vidéosurveillance: exemples de finalités, cas d'usage etc. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi', 3),
(4, 'biometrie', 't', 'Installation de dispositif biométrique', 'Dispositifs biométriques : exemples de finalités, cas d'usage etc. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi', 4) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_auto_typedemandeauto_finalites" ("id", "typedemandeauto_id", "finalite_id") VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 2, 7),
(6, 3, 5),
(7, 4, 6) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_categoriedemande" ("id", "label", "is_sensible", "description", "resume", "ordre", "niv_validation", "intitule_reponse") VALUES
(1, 'designation_dpo_physique', 'f', 'Désignation de Correspondant physique', ', 2, 3, 'Lettre d'approbation'),
(2, 'demande_autorisation', 'f', 'Demande d'autorisation', ', 0, 1, 'Décision'),
(3, 'designation_dpo_moral', 'f', 'Désignation de Correspondant personne morale', ', 2, 3, '),
(4, 'designation_dpo', 'f', 'Désignation de Correspondant', ', 1, 3, 'Lettre d'approbation') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_categoriedemande_types_reponses" ("id", "categoriedemande_id", "typereponse_id") VALUES
(1, 4, 1),
(2, 4, 2) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_commentaire" ("id", "created_at", "objet", "message", "is_new", "auteur_id", "demande_id") VALUES
(1, '2024-08-28 20:29:44.483857+00', 'Bonjour', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 't', 8, 1) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_critereevaluation" ("id", "label", "field_name", "field_type", "field_required", "categorie_demande_id") VALUES
(1, 'dossier_complet', 'Complétude du dossier', 'number', 't', 4),
(2, 'profil', 'Profil du Correspondant', 'number', 't', 4) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_demande" ("id", "created_at", "updated_at", "num_demande", "finished_at", "is_locked", "reponse_ok", "analyse_id", "categorie_id", "created_by_id", "organisation_id", "status_id", "updated_by_id") VALUES
(1, '2024-08-28 20:15:08.876675+00', '2024-08-28 20:15:08.876689+00', '20240828-000001', NULL, 'f', 't', 1, 4, 3, 3, 17, NULL),
(2, '2024-08-28 20:26:10.293017+00', '2024-08-28 20:26:10.293033+00', '20240828-000002', NULL, 'f', NULL, NULL, 4, 3, 4, 12, NULL) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_historiquedemande" ("id", "created_at", "is_private", "action_id", "auteur_id", "demande_id", "status_id") VALUES
(1, '2024-08-28 20:15:08.892232+00', 'f', 1, 3, 1, 12),
(2, '2024-08-28 20:16:16.415192+00', 'f', 2, 3, 1, 12),
(3, '2024-08-28 20:21:50.405012+00', 'f', 2, 3, 1, 12),
(4, '2024-08-28 20:26:10.303408+00', 'f', 1, 3, 2, 12),
(5, '2024-08-28 20:26:25.70603+00', 'f', 2, 3, 2, 12),
(6, '2024-08-28 20:28:48.14675+00', 'f', 4, 8, 1, 7),
(7, '2024-08-28 20:29:44.490423+00', 'f', 3, 8, 1, 7),
(8, '2024-08-28 20:30:03.556648+00', 't', 4, 8, 1, 18),
(9, '2024-08-28 20:30:34.974658+00', 't', 4, 9, 1, 14),
(10, '2024-08-28 20:31:05.419016+00', 't', 4, 10, 1, 15),
(11, '2024-08-28 20:31:32.041114+00', 't', 4, 11, 1, 11) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_reponsedemande" ("id", "created_at", "intitule", "titre_destinataire", "adresse_destinataire", "num_autorisation", "fichier_reponse", "signataire_id", "type_reponse_id") VALUES
(1, '2024-08-28 20:29:25.02386+00', 'Lettre d'approbation', NULL, NULL, NULL, 'docs/reponses/projet_reponse_correspondant_approbation.pdf', NULL, NULL) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_typereponse" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'lettre_approbation', 'f', 'Lettre d'approbation du Correspondant', ', 1),
(2, 'lettre_refus', 'f', 'Lettre de refus du Correspondant', ', 2),
(3, 'decision_autorisation', 'f', 'Décision d'autorisation de traitement', ', 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."demande_validationdemande" ("id", "created_at", "niveau_validation", "avis", "observations", "created_by_id") VALUES
(1, '2024-08-28 20:30:34.962569+00', 1, 't', ', 9),
(2, '2024-08-28 20:31:05.408802+00', 2, 't', ', 10),
(3, '2024-08-28 20:31:29.532071+00', 3, 't', ', 11) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."django_admin_log" ("id", "action_time", "object_id", "object_repr", "action_flag", "change_message", "content_type_id", "user_id") VALUES
(1, '2024-08-28 19:51:38.975704+00', '3', 'JOJO (Charles)', 1, '[{"added": {}}]', 6, 1),
(2, '2024-08-28 19:53:01.19274+00', '4', 'COCO (Simon)', 1, '[{"added": {}}]', 6, 1),
(3, '2024-08-28 19:53:20.329463+00', '4', 'COCO (Simon)', 2, '[]', 6, 1),
(4, '2024-08-28 19:54:12.824187+00', '5', 'TOTO (Carlos)', 1, '[{"added": {}}]', 6, 1),
(5, '2024-08-28 19:57:14.967421+00', '6', 'DPO1 (DPO1)', 1, '[{"added": {}}]', 6, 1),
(6, '2024-08-28 19:58:15.933835+00', '7', 'DPO2 (DPO2)', 1, '[{"added": {}}]', 6, 1),
(7, '2024-08-28 19:58:19.725554+00', '7', 'DPO2 (DPO2)', 2, '[]', 6, 1),
(8, '2024-08-28 19:59:28.695202+00', '8', 'Agent (No1)', 1, '[{"added": {}}]', 6, 1),
(9, '2024-08-28 19:59:38.095125+00', '8', 'Agent (No1)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(10, '2024-08-28 20:00:30.23078+00', '9', 'Superv (No1)', 1, '[{"added": {}}]', 6, 1),
(11, '2024-08-28 20:00:40.331474+00', '9', 'Superv (No1)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(12, '2024-08-28 20:01:22.326776+00', '10', 'Manager (No1)', 1, '[{"added": {}}]', 6, 1),
(13, '2024-08-28 20:01:28.514634+00', '10', 'Manager (No1)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(14, '2024-08-28 20:02:14.725135+00', '11', 'Directeur (Dir)', 1, '[{"added": {}}]', 6, 1),
(15, '2024-08-28 20:02:21.463388+00', '11', 'Directeur (Dir)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(16, '2024-08-28 20:03:04.249735+00', '12', 'Directeur (Général)', 1, '[{"added": {}}]', 6, 1),
(17, '2024-08-28 20:03:10.196346+00', '12', 'Directeur (Général)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(18, '2024-08-28 20:03:43.926795+00', '13', 'PCR (PCR)', 1, '[{"added": {}}]', 6, 1),
(19, '2024-08-28 20:03:52.384044+00', '13', 'PCR (PCR)', 2, '[{"changed": {"fields": ["Groups"]}}]', 6, 1),
(20, '2024-08-28 20:04:26.372713+00', '3', 'JOJO (Charles)', 2, '[{"changed": {"fields": ["Est Membre du Personnel"]}}]', 6, 1),
(21, '2024-08-28 20:05:49.41714+00', '1', 'SuperDPO SARL', 1, '[{"added": {}}]', 11, 1),
(22, '2024-08-28 20:06:56.530947+00', '2', 'Best DPO SA', 1, '[{"added": {}}]', 11, 1),
(23, '2024-08-28 20:08:50.724479+00', '3', 'JOJO SARLU', 1, '[{"added": {}}]', 11, 1),
(24, '2024-08-28 20:10:10.218621+00', '4', 'PME1', 1, '[{"added": {}}]', 11, 1),
(25, '2024-08-28 20:21:08.715982+00', '3', 'Commentaires', 1, '[{"added": {}}]', 18, 1),
(26, '2024-08-28 20:21:20.323128+00', '4', 'Changement de statut', 1, '[{"added": {}}]', 18, 1),
(27, '2024-08-28 20:24:15.442569+00', '1', 'SuperDPO SARL', 3, ', 11, 1),
(28, '2024-08-28 20:24:15.445887+00', '2', 'Best DPO SA', 3, ', 11, 1),
(29, '2024-08-28 20:25:10.997011+00', '5', 'SuperDPO SARL', 1, '[{"added": {}}]', 29, 1),
(30, '2024-08-28 20:25:48.993748+00', '6', 'Best DPO SA', 1, '[{"added": {}}]', 29, 1),
(31, '2024-08-28 20:28:05.751489+00', '4', 'PME1', 2, '[{"changed": {"fields": ["Num\u00e9ro RCCM", "A d\u00e9sign\u00e9 un Correspondant"]}}]', 11, 1),
(32, '2024-08-28 20:28:18.419739+00', '3', 'JOJO SARLU', 2, '[{"changed": {"fields": ["Num\u00e9ro d'IDentifiant Unique", "Num\u00e9ro RCCM", "A d\u00e9sign\u00e9 un Correspondant"]}}]', 11, 1) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."django_content_type" ("id", "app_label", "model") VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'base_edcp', 'user'),
(7, 'base_edcp', 'role'),
(8, 'base_edcp', 'notification'),
(9, 'base_edcp', 'journaltransaction'),
(10, 'base_edcp', 'groupextension'),
(11, 'base_edcp', 'enregistrement'),
(12, 'options', 'groupname'),
(13, 'options', 'pays'),
(14, 'options', 'secteur'),
(15, 'options', 'status'),
(16, 'options', 'typeclient'),
(17, 'options', 'typepiece'),
(18, 'demande', 'actiondemande'),
(19, 'demande', 'analysedemande'),
(20, 'demande', 'categoriedemande'),
(21, 'demande', 'demande'),
(22, 'demande', 'typereponse'),
(23, 'demande', 'validationdemande'),
(24, 'demande', 'reponsedemande'),
(25, 'demande', 'historiquedemande'),
(26, 'demande', 'critereevaluation'),
(27, 'demande', 'commentaire'),
(28, 'correspondant', 'agrementdcp'),
(29, 'correspondant', 'cabinetdpo'),
(30, 'correspondant', 'exerciceactivite'),
(31, 'correspondant', 'moyensdpo'),
(32, 'correspondant', 'qualificationsdpo'),
(33, 'correspondant', 'typedpo'),
(34, 'correspondant', 'designationdpomoral'),
(35, 'correspondant', 'correspondant'),
(36, 'demande_auto', 'demandeauto'),
(37, 'demande_auto', 'echellenotation'),
(38, 'demande_auto', 'finalite'),
(39, 'demande_auto', 'persconcernee'),
(40, 'demande_auto', 'demandeautobiometrie'),
(41, 'demande_auto', 'demandeautotraitement'),
(42, 'demande_auto', 'demandeautotransfert'),
(43, 'demande_auto', 'demandeautovideo'),
(44, 'demande_auto', 'typedemandeauto'),
(45, 'demande_auto', 'sousfinalite') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."django_migrations" ("id", "app", "name", "applied") VALUES
(1, 'contenttypes', '0001_initial', '2024-08-28 18:21:41.719076+00'),
(2, 'options', '0001_initial', '2024-08-28 18:21:41.763549+00'),
(3, 'contenttypes', '0002_remove_content_type_name', '2024-08-28 18:21:41.773308+00'),
(4, 'auth', '0001_initial', '2024-08-28 18:21:41.811311+00'),
(5, 'auth', '0002_alter_permission_name_max_length', '2024-08-28 18:21:41.817769+00'),
(6, 'auth', '0003_alter_user_email_max_length', '2024-08-28 18:21:41.824468+00'),
(7, 'auth', '0004_alter_user_username_opts', '2024-08-28 18:21:41.830861+00'),
(8, 'auth', '0005_alter_user_last_login_null', '2024-08-28 18:21:41.837671+00'),
(9, 'auth', '0006_require_contenttypes_0002', '2024-08-28 18:21:41.841043+00'),
(10, 'auth', '0007_alter_validators_add_error_messages', '2024-08-28 18:21:41.847655+00'),
(11, 'auth', '0008_alter_user_username_max_length', '2024-08-28 18:21:41.854098+00'),
(12, 'auth', '0009_alter_user_last_name_max_length', '2024-08-28 18:21:41.861748+00'),
(13, 'auth', '0010_alter_group_name_max_length', '2024-08-28 18:21:41.870486+00'),
(14, 'auth', '0011_update_proxy_permissions', '2024-08-28 18:21:41.879125+00'),
(15, 'auth', '0012_alter_user_first_name_max_length', '2024-08-28 18:21:41.885835+00'),
(16, 'base_edcp', '0001_initial', '2024-08-28 18:21:42.009746+00'),
(17, 'admin', '0001_initial', '2024-08-28 18:21:42.037761+00'),
(18, 'admin', '0002_logentry_remove_auto_add', '2024-08-28 18:21:42.048402+00'),
(19, 'admin', '0003_logentry_add_action_flag_choices', '2024-08-28 18:21:42.059768+00'),
(20, 'demande', '0001_initial', '2024-08-28 18:21:42.577193+00'),
(21, 'correspondant', '0001_initial', '2024-08-28 18:21:42.614261+00'),
(22, 'correspondant', '0002_initial', '2024-08-28 18:21:42.791136+00'),
(23, 'demande_auto', '0001_initial', '2024-08-28 18:21:43.259126+00'),
(24, 'sessions', '0001_initial', '2024-08-28 18:21:43.276189+00') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."django_session" ("session_key", "session_data", "expire_date") VALUES
('epx8tafa5tl0u6po07x8pym4v18gntok', '.eJxVjMsOwiAURP-FtSFwQR4u3fsN5MKlUjWQlHZl_HdL0oUu58yZebOA21rC1vMSZmIXJtnpl0VMz1xHQQ-s98ZTq-syRz4UfrSd3xrl1_Vw_w4K9rKvlYyWEghrdPQKDbkkPQkTk3UGQFsx4QROk5PnrDDvESNIHFB5C-zzBdkjN8Q:1sjP6q:LfJDB456wmY1aEf0HGqSTn7YNkzf4DjknpZzGDDIymE', '2024-09-11 20:17:40.165882+00'),
('m0ar8cj2v29lzgazkrh4xst6x1cm0j23', '.eJxVjMsOwiAQRf-FtSG8KS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZlJyU6_I0J6UNtJvkO7dZ56W5cZ-a7wgw5-7Zmel8P9O6gw6rcmW9BI54y1qShQEBBEkJqsIQWT00lMQZLL6LV2IgeDXoGXAnQoGBx7fwD-djeg:1sjPK4:xe5z4mYBh4-Yu9xyBIwg0t_LYLTrAr2J8suITdYlods', '2024-09-11 20:31:20.962018+00') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_groupname" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'agents', 'f', 'Agents', ', 1),
(2, 'superviseurs', 'f', 'Superviseurs (CS)', ', 2),
(3, 'managers', 'f', 'Managers (CD)', ', 3),
(4, 'directeur', 'f', 'Directeur', ', 4),
(5, 'directeur_general', 'f', 'Directeur Général', ', 5),
(6, 'president', 'f', 'Président du Conseil de Régulation', ', 6) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_pays" ("id", "label") VALUES
(1, 'Côte d'Ivoire'),
(2, 'Burkina Faso'),
(3, 'Mali'),
(4, 'Ghana'),
(5, 'Nigeria'),
(6, 'Bénin'),
(7, 'Togo') ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_secteur" ("id", "label", "sensible", "ordre") VALUES
(1, 'Banque', 'f', 0),
(2, 'Assurance', 'f', 0),
(3, 'Santé', 't', 0),
(4, 'Informatique', 'f', 0),
(5, 'Communication', 'f', 0),
(6, 'Industrie', 'f', 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_status" ("id", "label", "is_sensible", "description", "resume", "ordre") VALUES
(1, 'brouillon', 'f', 'Brouillon', ', 1),
(2, 'demande_en_cours_traitement', 'f', 'En cours de traitement', ', 2),
(3, 'demande_attente_complement', 'f', 'Suspendue (en attente de compléments d'information)', ', 3),
(4, 'demande_attente_paiement', 'f', 'Validée (en attente de paiement)', ', 4),
(5, 'demande_attente_decision', 'f', 'Payée (en attente de la décision)', ', 5),
(6, 'termine', 'f', 'Terminé', ', 6),
(7, 'analyse_en_cours', 'f', 'Analyse en cours', ', 1),
(9, 'attente_analyse_technique', 'f', 'En attente d'analyse technique', ', 0),
(10, 'attente_analyse_juridique', 'f', 'En attente d'analyse juridique', ', 0),
(11, 'analyse_terminee', 'f', 'Analyse terminée', ', 0),
(12, 'demande_attente_traitement', 'f', 'En attente de traitement', ', 0),
(13, 'analyse_attente_validation_1', 'f', 'En attente de validation niv. 1', ', 0),
(14, 'analyse_attente_validation_2', 'f', 'En attente de validation niv. 2', ', 0),
(15, 'analyse_attente_validation_3', 'f', 'En attente de validation niv. 3', ', 0),
(16, 'analyse_attente_corrections', 'f', 'Analyse en attente de corrections', ', 0),
(17, 'traitement_termine', 'f', 'Traitement terminé', ', 0),
(18, 'attente_validation_1', 'f', 'En attente de validation niv. 1', ', 0),
(19, 'analyse_attente_validation_4', 'f', 'En attente de validation niv. 4', ', 0),
(20, 'attente_validation_2', 'f', 'En attente de validation niv. 2', ', 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_typeclient" ("id", "label", "description", "sensible", "ordre") VALUES
(1, 'Personne physique', 'Personne physique', 'f', 0),
(2, 'PME', 'Petite ou moyenne entreprise', 'f', 0),
(3, 'Grande entreprise', 'Grande entreprise', 'f', 0),
(4, 'Administration', 'Administration', NULL, 0) ON CONFLICT (id) DO NOTHING;

INSERT INTO "public"."options_typepiece" ("id", "label", "description", "sensible", "ordre") VALUES
(1, 'CNI', ', 'f', 0),
(2, 'Passeport', 'f', 0),
(3, 'Permis de conduire', ', 'f', 0) ON CONFLICT (id) DO NOTHING;

