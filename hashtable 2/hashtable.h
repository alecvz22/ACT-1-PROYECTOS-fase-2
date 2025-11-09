using namespace std;

class HashTable {
public:
   HashTable (const HashTable& ht );       // constructor for a copy
   HashTable(const long Size);          // constructor of hashtable 
   ~HashTable();                           // destructor
   void WriteData (string Path);
   long FindLocation(long Index);
   void UpdateLocation(long Location, long NewValue);
   void UpdateNumDocs(long Location, int Decrease);
   long Insert (const string Key, int LasDocID, long PfMaxVal); 
//protected:
   struct StringIntPair // the datatype stored in the hashtable`
   {
      string key;
      int numdocs;
	  long start;
	  int lastdocid;
   };
   long Find (const string Key); // the index of the ddr in the hashtable
//private:
   StringIntPair *hashtable;        // the hashtable array itself
    long size;              // the hashtable size
    long used;
    long collisions;
    long lookups;
};

class PostingFile {
public:
   //HashTable (const HashTable& ht );       // constructor for a copy
   PostingFile(const long Size);          // constructor of hashtable 
   ~PostingFile();                           // destructor
   void ShowData(string Path);
   void Insert (int LastDocID, const long Start, float Weight); 
   
   string PrintFrom(long Start, long &Counter,  int &Decrease);
   
	long FindMax (); 
//protected:
   struct StringIntPair // the datatype stored in the hashtable`
   {
      int docid;
      long freq;
	  float weight;
	  long next;
   };
   long Find (const string Key); // the index of the ddr in the hashtable
//private:
   StringIntPair *postingfile;        // the hashtable array itself
    long size;              // the hashtable size
    long used;
    long collisions;
    long lookups;
};

class Documents {
public:
   //HashTable (const HashTable& ht );       // constructor for a copy
   Documents(const long Size);          // constructor of hashtable 
   ~Documents();                           // destructor
   void ShowData();
   void WriteData(string Path);
   int Insert (const string DocName, const long Tokens); 
//protected:
   struct StringIntPair // the datatype stored in the hashtable`
   {
      int docid;
      string docname;
	  unsigned long tokens;
   };
   long Find (const string Key); // the index of the ddr in the hashtable
//private:
   StringIntPair * documents;        // the hashtable array itself
    long size;              // the hashtable size
    long used;
    long collisions;
    long lookups;
};
