/**
 * @file parser.h
 * @author pierre marchand (marchand.pierre63@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2021-06-16
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef PARSER_H
#define PARSER_H
/**
 * @brief Mise en forme de la commande à envoyer
 * 
 * @param command commande à envoyer
 * @param ppParams liste des parametres a ajouter
 * @param numParams nombre de paramètres
 */
    void send_command(char *command, char **ppParams, int numParams);
    void config_modem(void);
    void timer_cb(void);
#endif