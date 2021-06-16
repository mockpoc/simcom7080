/**
 * @file main.c
 * @author pierre (pierre.marchand63@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2021-06-16
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include "test.h"
#include <stdio.h>
#include "unity.h"

/**
 * @brief Execute le test sdu SIMCOM7080
 * 
 * @return int code erreur du soft de test
 */
int main(void)
{
    UnityBegin("parser.c");
    RUN_TEST(test_parser);

    // TODO Ecrire le test
    return (UnityEnd());
}