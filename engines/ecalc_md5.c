#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>
//#include <unistd.h>
//#include <sys/types.h>

void bytes2md5(const char *data, int len, char *md5buf) {
  // Based on https://www.openssl.org/docs/manmaster/man3/EVP_DigestUpdate.html
  EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
  const EVP_MD *md = EVP_md5();
  unsigned char md_value[EVP_MAX_MD_SIZE];
  unsigned int md_len, i;
  EVP_DigestInit_ex(mdctx, md, NULL);
  EVP_DigestUpdate(mdctx, data, len);
  EVP_DigestFinal_ex(mdctx, md_value, &md_len);
  EVP_MD_CTX_destroy(mdctx);
  for (i = 0; i < md_len; i++) {
    snprintf(&(md5buf[i * 2]), 16 * 2, "%02x", md_value[i]);
  }
}

char * return_md5(int len, char *data) {
  //const char *hello = "Abcd";
  const char characters[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  int characters_len = strlen(characters);
  char* answer = (char*)malloc(len * sizeof(char));
  char md5[33]; // 32 characters + null terminator
  unsigned int literals_index[len+1];
  char literals[len];
  for(int i=0;i<=len;i++){
    literals_index[i]=0;
  }
  int i = 0;
  short flag = 1;
  while(flag)
  {
    for(int j = 0; j<len; j++)
    {
      literals[j] = characters[literals_index[j]];
    }
    literals[len] = '\0';
    bytes2md5(literals, strlen(literals), md5);
    if (!strcmp(data, md5)){
      strcpy(answer, literals);
      //printf("The PID of C is: %i\n", getpid());
      return answer;
    }
    literals_index[0]++;
    if (literals_index[0] == characters_len)
    {
      for(int j =0 ; j<=i; j++)
      {
        if (literals_index[j] == characters_len)
        {
          literals_index[j] =0;
          literals_index[j+1]++;
            i = j+1;
        }
      }
    }
    if(literals_index[len] == 1)
    {
      flag = 0;
    }
  }
  strcpy(answer, "None");
  //pid_t id;
  //id = getpid();
  //printf("The PID of C is: %i\n", getpid());
  return answer;
}

// int main(void) {
//   const char *hello = "hello";
//   char md5[33]; // 32 characters + null terminator
//   bytes2md5(hello, strlen(hello), md5);
//   printf("%s\n", md5);
// }

//gcc -shared -I /usr/bin/ssl example_md5.c -Wl,-soname,adder -o ex.so -Wl,-rpath /usr/bin/lib -Wl,-L,/usr/bin/lib -lssl -lcrypto