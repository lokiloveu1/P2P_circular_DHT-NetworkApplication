/* 
 * File:   MyDDList.c
 * Author: loki
 * Student Name: Qian Cheng
 * Student ID: z5149155
 * Created on 25 March 2018, 5:21 PM
 */

#include <stdio.h>
#include <assert.h>
#include <curses.h>
#include <stdlib.h>
#include <string.h>
// all the basic data structures and functions are included in this template
// you can add your own auxiliary functions as you like 

// data structures representing DLList

// data type for nodes
typedef struct DLListNode {
	int  value;  // value (int) of this list item 
	struct DLListNode *prev;
	// pointer previous node in list
	struct DLListNode *next;
	// pointer to next node in list
} DLListNode;

//data type for doubly linked lists
typedef struct DLList{
	int  size;      // count of items in list
	DLListNode *first;  // first node in list
	DLListNode *last;  // last node in list
} DLList;

// create a new DLListNode
DLListNode *newDLListNode(int it)
{
	DLListNode *new;
	new = malloc(sizeof(DLListNode));
	assert(new != NULL);
	new->value = it;
	new->prev = new->next = NULL;
	return new;
}

// create a new empty DLList
DLList *newDLList()
{
	struct DLList *L;
	L = malloc(sizeof (struct DLList));
	assert (L != NULL);
	L->size = 0;
	L->first = NULL;
	L->last = NULL;
	return L;
}


// create a DLList from a text file
// O(n).put your time complexity analysis for CreateDLListFromFileDlist() here
DLList *CreateDLListFromFileDlist(const char *filename)
{
  DLList *L ;
  L = newDLList();  //generate a new ddlist
  DLListNode *new;  //generate a new node
  DLListNode *next;  //next node
  DLListNode *prev;  //prev node
  next = L->first;
  prev = L->last;
  int n=0;
  int number = 0;
  char line[10];
  char line2[10];
  FILE *filen;
  //filen= malloc(sizeof (struct DLList));
  if (filename == "stdin"){   //input generate
      while (fgets(line, sizeof line, stdin) != NULL && (line[0] != '\n')){
                number = atoi(line);
                if(L->size ==0){                       //generate first node
                    next = newDLListNode(number);
                    next->prev = NULL;
                    L->first = next;
                    L->size++;
                }
                else{
                    while (next->next!=NULL){     //for each input number generate a new node and link it
                        next = next->next;
                    }
                    next->next = newDLListNode(number);
                    prev = next;
                    next = next->next;
                    next->prev = prev;
                    L->last = next;
                    next->next = NULL;
                }
        }
        return L;
  }
  else{  //file open and generate
      filen = fopen(filename, "r");
      while (fscanf(filen,"%s", line2)!=EOF) {
        n = atoi(line2);
	new = newDLListNode(n);
	if (L->last == NULL) {
                new->prev = NULL;
		L->first = L->last = new;
        }
	else {
		L->last->next = new;
		new->prev = L->last;
		L->last = new;
                new ->next=NULL;
	}
	L->size++; //size of ddlist
    }	
      fclose(filen); // close file
  }
    return L;
}


// clone a DLList
// O(n).put your time complexity analysis for cloneList() here
DLList *cloneList(struct DLList *u)
{
    DLList *L;  //generate a new ddlist
    L=newDLList();  //generate a new ddlist
    if (u == NULL) 
      L = u; 
    DLListNode *nodeinLp,*nodeinLn, *nodeinu; //generate a new node in L and u.
    int v;
    //nodeinL, nodeinu = malloc(sizeof(DLListNode));
    nodeinu = u->first;
    if (nodeinu != NULL) { //u is not null
        nodeinLn = newDLListNode(nodeinu->value); //node in L next 
        L->first = nodeinLn;
        nodeinLn->prev = NULL;
        nodeinu = nodeinu->next;    
    }
    while (nodeinu!=NULL){ //define rest nodes 
        v = nodeinu->value;  //v = node in u 's value
        nodeinLn->next = newDLListNode(v);
        nodeinLp = nodeinu;
        nodeinLn = nodeinLn->next;
        nodeinLn->prev=nodeinLp;
        L->last = nodeinLn;
        nodeinu = nodeinu->next;
    }
    return L;
}


// compute the union of two DLLists u and v
// O(u*v).
DLList *setUnion(struct DLList *u, struct DLList *v)
{
    DLList *L;
    L = cloneList(u);     //temp dllist
    DLListNode* nodeinu;
    nodeinu = L->first;
    DLListNode* nodeinv;
    nodeinv = v->first;
    DLListNode* temo;
    int c = 0;  //switch
    while(nodeinv != NULL){ //v is not null
        while (nodeinu->next != NULL){ 
            if (nodeinv->value == nodeinu->value){ //
                c = 1; //switch
            }
            nodeinu = nodeinu->next; //next
        }
        if (c == 0){ //no match
            temo = nodeinu; 
            nodeinu->next = newDLListNode(nodeinv->value);
            nodeinu = nodeinu->next;
            nodeinu->prev = temo;
        }
        c = 0; //reset
        nodeinv = nodeinv->next;
        nodeinu = L->first;
    }
    return L; 
}


// compute the insection of two DLLists u and v
// O(u*v).put your time complexity analysis for intersection() here
DLList *setIntersection(struct DLList *u, struct DLList *v)
{ 
    DLList *L;
    L= newDLList();
    DLListNode* nodeinL; //generate a new node in L and u and v.
    nodeinL = L->first;
    DLListNode* nodeinu;
    nodeinu = u->first;  
    DLListNode* nodeinv;    
    nodeinv = v->first;
    DLListNode* temp;
    int c = 0; //count time
    while(nodeinv ->next != NULL){
        while (nodeinu->next != NULL){
            if (nodeinv->value == nodeinu->value){
                if (c == 0){ //first node
                    nodeinL = newDLListNode(nodeinv->value);
                    L->first = nodeinL;       
                    nodeinL->prev = NULL;
                    nodeinL->next = NULL;
                    c++;
                }
                else{ //define rest node
                    nodeinL->next = newDLListNode(nodeinv->value);
                    temp = nodeinL;
                    nodeinL = nodeinL->next;
                    nodeinL->prev = temp;
                }
            }
            nodeinu = nodeinu->next; //next node
        }
        nodeinu = u->first;
        nodeinv = nodeinv->next;
    }
    nodeinL->next = NULL;
    return L;
}


// free up all space associated with list
// put your time complexity analysis for freeDLList() here
void freeDLList(struct DLList *L)
{
    assert(L != NULL);  //assert L is not null
    DLListNode *curr, *prev; //generate node current/previous
    curr = L->first;
    while (curr != NULL) {
	prev = curr;
	curr = curr->next;
	free(prev);  //free node
    }
    free(L); //free dllist
}


// display items of a DLList
// put your time complexity analysis for printDDList() here
void printDLList(struct DLList *u)
{
  DLListNode* curr;   //generate node current
  curr = u->first;
  while (curr->next != NULL)  //while current exist
  { 
    printf("Element: %d \n", curr->value);  //print current node pre line
    curr = curr -> next;   
  }
  printf("Element: %d \n", curr->value);  //print last node
}

int main()
{
 DLList *list1, *list2, *list3, *list4;
 
 list1=CreateDLListFromFileDlist("File1.txt");
 printDLList(list1);
 
 list2=CreateDLListFromFileDlist("File2.txt");
 printDLList(list2);

 list3=setUnion(list1, list2);
 printDLList(list3);

 list4=setIntersection(list1, list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 printf("please type all the integers of list1\n");
 list1=CreateDLListFromFileDlist("stdin");

 printf("please type all the integers of list2\n");
 list2=CreateDLListFromFileDlist("stdin");

 list3=cloneList(list1);
 printDLList(list3);
 list4=cloneList(list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 return 0; 
}
