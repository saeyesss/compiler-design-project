//Q2: Find the largest number using if statement
int main(){
    int n1, n2, n3;
    if(n1 >= n2){
        if(n1 >= n3){
            printf("%d", n1);
        }
        else{
            printf("%d", n3);
        }
    } else{
        if(n2 >= n3){
            printf("%d", n2);
        }
        else{
            printf("%d", n3);
        }
    }
}