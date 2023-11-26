#include <bits/stdc++.h>
#define ll long long
using namespace std;

void readNumbersFromFile(const string& fileName, vector<ll>& numbers, ll& mx_num) {
    ifstream file(fileName);
    string tt, str;
    ll tmp;

    while (getline(file, tt)) {
        stringstream sst(tt);
        getline(sst, str, ':');
        getline(sst, str, '\n');
        stringstream ss(str);
        ss >> tmp;
        mx_num = max(mx_num, tmp);
        numbers.push_back(tmp);
    }

    file.close();
}

int main(){
	system("hashcat -m 0 -a 3 hashed_numbers.txt ?d?d?d?d?d?d?d?d?d?d?d -o unhashed_numbers.txt --show");
    	vector<ll> numbers;
	vector<ll> dict = {89156617519, 89866878664, 89636187893, 89038679411, 89868468991};
    	string str, tt;
    	ll tmp, mx_num = 0;
    	readNumbersFromFile("unhashed_numbers.txt", numbers, mx_num);
    	vector<ll> salts;
    	for (const auto &x : numbers) {
		for (const auto &y : dict) salts.push_back(y-x);
    	}
    	ll ans_salt;
    	for (const auto &salt : salts) {
		vector<bool> k(dict.size(), false);
		for (const auto &x : numbers) {
	    		for (ll i = 0; i < dict.size(); ++i) {
				if (x+salt == dict[i]) k[i] = true;
	    		}
		}
		ll sm = 0;
		for (const auto &x : k) sm += x;
		if (sm == dict.size()) {
	    		cout << "Salt = " << -salt << endl;
	    		ans_salt = salt;
	    		break;
		}
    	}
    	ofstream out("numbers.txt");
    	for (auto &element : numbers) {
		out << element + ans_salt << endl;
    	}
    	out.close();
}
