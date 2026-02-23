#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX 20000

// merges two sorted parts of the array
void merge(int arr[], int left, int mid, int right){

    int n1 = mid-left+1;   // size of first part
    int n2 = right-mid;    // size of second part

    int L[n1], R[n2];      // temporary arrays

    // copy first part
    for(int i=0;i<n1;i++)
        L[i]=arr[left+i];

    // copy second part
    for(int j=0;j<n2;j++)
        R[j]=arr[mid+1+j];

    int i=0,j=0,k=left;

    // compare elements and merge
    while(i<n1 && j<n2){

        if(L[i]<=R[j]){
            arr[k]=L[i];
            i++;
        }
        else{
            arr[k]=R[j];
            j++;
        }
        k++;
    }

    // copy remaining elements from L
    while(i<n1){
        arr[k]=L[i];
        i++; k++;
    }

    // copy remaining elements from R
    while(j<n2){
        arr[k]=R[j];
        j++; k++;
    }
}

// divides array and sorts recursively
void mergeSort(int arr[], int left, int right){

    if(left<right){

        int mid=(left+right)/2;   // middle position

        mergeSort(arr,left,mid);      // sort left part
        mergeSort(arr,mid+1,right);   // sort right part

        merge(arr,left,mid,right);    // merge parts
    }
}


// finds the maximum value in array
int findMax(int arr[], int n){

    int max=arr[0];

    for(int i=1;i<n;i++)
        if(arr[i]>max)
            max=arr[i];

    return max;
}

// counting sort algorithm
void countSort(int arr[], int n){

    int max=findMax(arr,n);  // maximum value

    int count[max+1];

    // set counters to zero
    for(int i=0;i<=max;i++)
        count[i]=0;

    // count occurrences
    for(int i=0;i<n;i++)
        count[arr[i]]++;

    // cumulative counts
    for(int i=1;i<=max;i++)
        count[i]+=count[i-1];

    int output[n];

    // build sorted array
    for(int i=n-1;i>=0;i--){
        output[count[arr[i]]-1]=arr[i];
        count[arr[i]]--;
    }

    // copy back to original
    for(int i=0;i<n;i++)
        arr[i]=output[i];
}


// divides array around pivot
int partition(int arr[], int start, int end){

    int pivot=arr[end];  // pivot element
    int index=start;

    for(int i=start;i<end;i++){

        if(arr[i]<=pivot){

            int temp=arr[i];
            arr[i]=arr[index];
            arr[index]=temp;

            index++;
        }
    }

    // put pivot in correct position
    int temp=arr[end];
    arr[end]=arr[index];
    arr[index]=temp;

    return index;
}

// quick sort algorithm
void quickSort(int arr[], int start, int end){

    if(start<end){

        int p=partition(arr,start,end);

        quickSort(arr,start,p-1);  // left side
        quickSort(arr,p+1,end);    // right side
    }
}


// keeps heap property
void heapify(int arr[], int n, int i){

    int largest=i;

    int left=2*i+1;
    int right=2*i+2;

    // check left child
    if(left<n && arr[left]>arr[largest])
        largest=left;

    // check right child
    if(right<n && arr[right]>arr[largest])
        largest=right;

    // swap if needed
    if(largest!=i){

        int temp=arr[i];
        arr[i]=arr[largest];
        arr[largest]=temp;

        heapify(arr,n,largest);
    }
}

// heap sort algorithm
void heapSort(int arr[], int n){

    // build heap
    for(int i=n/2-1;i>=0;i--)
        heapify(arr,n,i);

    // extract elements
    for(int i=n-1;i>0;i--){

        int temp=arr[0];
        arr[0]=arr[i];
        arr[i]=temp;

        heapify(arr,i,0);
    }
}


// generates random numbers
void generateArray(int arr[], int n){

    for(int i=0;i<n;i++)
        arr[i]=rand()%1000;
}

// copies array
void copyArray(int a[], int b[], int n){

    for(int i=0;i<n;i++)
        b[i]=a[i];
}


int main(){

    srand(time(NULL));  // random seed

    int sizes[]={100,1000,5000,10000,20000};

    int original[MAX];
    int test[MAX];

    clock_t start,end;

    for(int s=0;s<5;s++){

        int n=sizes[s];

        generateArray(original,n);

        printf("\nSize %d\n",n);


        copyArray(original,test,n);
        start=clock();
        quickSort(test,0,n-1);
        end=clock();
        printf("Quick %f\n",
        (double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        mergeSort(test,0,n-1);
        end=clock();
        printf("Merge %f\n",
        (double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        heapSort(test,n);
        end=clock();
        printf("Heap %f\n",
        (double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        countSort(test,n);
        end=clock();
        printf("Count %f\n",
        (double)(end-start)/CLOCKS_PER_SEC);

    }

    return 0;
}