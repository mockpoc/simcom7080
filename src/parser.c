/**
 * @file parser.c
 * @author pierre marchand (marchand.pierre63@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2021-06-16
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include <stdio.h>
#include <string.h>
#include "at_engine.h"
#ifdef TEST
    FILE *pFile;
#endif
/**
 * @brief Wrapper pouvant être remplacé par l'écriture sur la liaison série
 * 
 * @param pBuffer string terminé par '\0' à envoyer
 */
void write_func(char *pBuffer)
{
    #ifdef TEST
        fwrite(pBuffer,1, strlen(pBuffer), pFile);
    #endif
}

void send_command(char *command, char** ppParams, int numParams)
{
    /* Le buffer permet de mettre en forme avec le nom de la commande							*/
    
    /* Si on est en test, alors le buffer d'écriture sera un fichier							*/
    #ifdef TEST
        pFile = fopen("write.dump", "wb");
    #endif

    write_func(command);

    if(numParams > 0)
    {
        write_func(": ");
        for(int i = 0; i < numParams; i++)
        {
            write_func(ppParams[i]);
            if(i < (numParams - 1))
            {
                write_func(",");
            }
        }
    }
    write_func("\r\n");
    #ifdef TEST
    fclose(pFile);
    #endif
}

void get_response(char *pResponse, size_t buffLen)
{
}

void UART_write(unsigned char data_out)
{
    printf("TX:%c\n", data_out);
}

void C4G_defaultHandler( char *buffer, uint8_t *type )
{
    #ifdef TEST
    printf( "Response : \r\n" );
    printf( buffer );
    printf( "\r\n" );
    if( !strncmp( "\r\nRING", buffer, 6 ) )
        printf("received ring\n");
        // callFlag = true;
    #endif
}

void C4G_callerATHandler( char *rsp, uint8_t *flag )
{
    // char *tmpStart;
    // char *tmpEnd;

    // tmpStart = strchr( rsp, '\"' );
    // tmpEnd = strchr( tmpStart + 1, '\"' );
    // strncpy( callerId, tmpStart, tmpEnd - tmpStart + 1 );
    printf("AT handler !\n");
}

uint8_t bufferReception[1024];
static T_AT_storage storage[ 20 ];

void config_modem(void)
{
    printf("config ...\n");
    AT_initParser(UART_write, C4G_defaultHandler, 500, bufferReception, sizeof(bufferReception), storage, 20 );
    AT_saveHandler( "+AT", 500, C4G_callerATHandler );
    printf("init done\n");
    AT_cmdSingle( "AT" );
    AT_cmdSingle( "AT+CSCS=\"GSM\"" );
    AT_cmdSingle( "AT+CMGF=1" );
    AT_cmdSingle( "AT+CSCA?" );
    AT_cmdSingle( "AT+UGPIOC?" );
}