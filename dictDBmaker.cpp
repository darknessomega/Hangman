//termsql command:  termsql -d '+' -c word,pos,def -i "newtest.txt" -o "dictionary.db" -t dict -p '    '

#include <fstream>
#include <string>
#include <iostream>

using namespace std;

int main()
{

	ifstream oldTxt;
	ofstream newTxt;
	
	oldTxt.open("azdictionary.txt");
	newTxt.open("new_azdictionary.txt");

	string oldData = "", word = "", pos = "", def = "";
	int index = 0, line = 0, looper, looper2;

	
	while (!oldTxt.eof())
	{
		getline (oldTxt, oldData);
		looper = oldData.length();
		looper2 = oldData.length();
		index = 0;
		
		while (looper > 0)
		{
			if (oldData[index] != '(')
			{
				index++;
			}
			looper--;
		}
		if (oldData[index] == '(')
		{
			oldData[index - 1] = '+';
		}
			
		
		index = 0;
		while (looper2 > 0)
		{
			if (oldData[index] != ')')
			{
				index++;
			}
			looper2--;
		}
		if (oldData[index] == ')')
		{
			oldData [index + 1] = '+';
		}

		
		if (oldData[oldData.length() - 1] == '.')
		{
			oldData += '+';
			newTxt << oldData << endl;
		}
		else
		{		
			newTxt << oldData;
		}
	}
	oldTxt.close();
	newTxt.close();
}
