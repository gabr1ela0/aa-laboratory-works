#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX 100000  // max array size

// Merge Sort
// merge two sorted parts
void merge(int arr[], int left, int mid, int right){

    int n1 = mid-left+1;   // left size
    int n2 = right-mid;    // right size

    int L[n1], R[n2];      // temp arrays

    // copy left part
    for(int i=0;i<n1;i++)
        L[i]=arr[left+i];

    // copy right part
    for(int i=0;i<n2;i++)
        R[i]=arr[mid+1+i];

    int i=0,j=0,k=left;

    // merge back
    while(i<n1 && j<n2){

        if(L[i]<=R[j])
            arr[k++]=L[i++];
        else
            arr[k++]=R[j++];
    }

    // remaining left
    while(i<n1)
        arr[k++]=L[i++];

    // remaining right
    while(j<n2)
        arr[k++]=R[j++];
}

// recursive split
void mergeSort(int arr[], int left, int right){

    if(left<right){

        int mid=(left+right)/2; // middle

        mergeSort(arr,left,mid);
        mergeSort(arr,mid+1,right);

        merge(arr,left,mid,right);
    }
}


// Counting Sort
// find the biggest number
int findMax(int arr[], int n){

    int max=arr[0];

    for(int i=1;i<n;i++)
        if(arr[i]>max)
            max=arr[i];

    return max;
}

// counting sort
void countSort(int arr[], int n){

    int max=findMax(arr,n);

    int *count = (int*)calloc(max+1,sizeof(int)); // counter array
    int *output = (int*)malloc(n*sizeof(int));    // sorted array

    // count numbers
    for(int i=0;i<n;i++)
        count[arr[i]]++;

    // cumulative count
    for(int i=1;i<=max;i++)
        count[i]+=count[i-1];

    // build sorted array
    for(int i=n-1;i>=0;i--){
        output[count[arr[i]]-1]=arr[i];
        count[arr[i]]--;
    }

    // copy back
    for(int i=0;i<n;i++)
        arr[i]=output[i];

    free(count);
    free(output);
}


// Quick Sort
// split array around pivot
int partition(int arr[], int start, int end){
    int pivot=arr[end];   // pivot value
    int index=start;
    for(int i=start;i<end;i++){
        if(arr[i]<=pivot){
            int temp=arr[i];
            arr[i]=arr[index];
            arr[index]=temp;
            index++;
        }
    }
    // place pivot
    int temp=arr[end];
    arr[end]=arr[index];
    arr[index]=temp;

    return index;
}

// recursive quicksort
void quickSort(int arr[], int start, int end){
    if(start<end){
        int p=partition(arr,start,end);
        quickSort(arr,start,p-1);
        quickSort(arr,p+1,end);
    }
}


// Heap Sort
// keep heap property
void heapify(int arr[], int n, int i){

    int largest=i;

    int left=2*i+1;
    int right=2*i+2;

    // check children
    if(left<n && arr[left]>arr[largest])
        largest=left;

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

// heap sort
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


// generate random numbers
void generateArray(int arr[], int n){
    for(int i=0;i<n;i++)
        arr[i]=rand()%1000;
}

// copy array
void copyArray(int a[], int b[], int n){

    for(int i=0;i<n;i++)
        b[i]=a[i];
}


int main(){

    srand(time(NULL)); // random seed

    int sizes[]={100,1000,5000,10000,20000,50000,100000};

    int original[MAX];
    int test[MAX];

    clock_t start,end;

    // test all sizes
    for(int s=0;s<7;s++){

        int n=sizes[s];

        generateArray(original,n);

        printf("\nSize %d\n",n);


        copyArray(original,test,n);
        start=clock();
        quickSort(test,0,n-1);
        end=clock();
        printf("Quick %f\n",(double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        mergeSort(test,0,n-1);
        end=clock();
        printf("Merge %f\n",(double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        heapSort(test,n);
        end=clock();
        printf("Heap %f\n",(double)(end-start)/CLOCKS_PER_SEC);


        copyArray(original,test,n);
        start=clock();
        countSort(test,n);
        end=clock();
        printf("Count %f\n",(double)(end-start)/CLOCKS_PER_SEC);
    }

    return 0;
}