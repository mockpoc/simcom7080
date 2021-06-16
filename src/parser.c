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