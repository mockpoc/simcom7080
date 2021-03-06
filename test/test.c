/**
 * @file test.c
 * @author pierre (marchand.pierre63@gmail.com)
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
#include "stdbool.h"
#include <stdlib.h>
#include "parser.h"
#include <string.h>

/* Buffer contenant les données lues dans le fichier de parse									*/

char *pBuffer;

/**
 * @brief Set the Up object
 * 
 */
void setUp(void)
{
    // printf("Start\n");
}

/**
 * @brief nettoyage apres le test
 * 
 */
void tearDown(void)
{
    // printf("Done !\n");
}


void get_result(void)
{
    FILE *fp = fopen("write.dump","rb");
    fseek(fp, 0, SEEK_END);
    int idx = ftell(fp);
    rewind(fp);
    pBuffer = calloc(idx, 1);
    fread(pBuffer, 1, idx, fp);
    fclose(fp);
}
/**
 * @brief Test du format des commandes
 * 
 */
void test_send_command(void)
{
    /* Test envoi de la commande AT																*/
    send_command("AT", NULL, 0);
    get_result();
    TEST_ASSERT_EQUAL_STRING("AT\r\n", pBuffer);
    free(pBuffer);
    /* Test envoi de la commande CGATT															*/
    char *pParams[2] = {"0", "1"};
    send_command("AT+CGATT", pParams, 2);
    get_result();
    TEST_ASSERT_EQUAL_STRING("AT+CGATT: 0,1\r\n", pBuffer);
    free(pBuffer);
}

char bufferRx[1024];
void mock_event(void)
{
    // TODO c'est le bordel
    static int i = 0;
    printf("mock event\n");
    AT_tick();
    for (int i = 0 ; i < 10; i++)
    {
        AT_getChar(bufferRx[i]);
    }
    if(i > 20)
        exit(0);
}

void test_modem(void)
{
    strcpy(bufferRx, "AT\r\r\nOK\r\n");
    config_modem();
}