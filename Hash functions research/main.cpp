#include <bits/stdc++.h>
#define ll long long
using namespace std;

int main(){
	system("hashcat -m 0 -a 3 hashed_numbers.txt ?d?d?d?d?d?d?d?d?d?d?d -o unhashed_numbers.txt --show");
    vector<ll> numbers, salts;
    vector<ll> dict = {89156617519, 89866878664, 89636187893, 89038679411, 89868468991};
    string str, tt;
    ll tmp, ans_salt, mx_num = 0;
    ifstream file("unhashed_numbers.txt");
    while (getline(file, tt)) {
        stringstream sst(tt);
        getline(sst, str, ':');
        getline(sst, str, '\n');
        stringstream ss(str);
        ss >> tmp;
        mx_num = max(mx_num, tmp);
        numbers.push_back(tmp);
    }
    file.close()
    for (const auto &x : numbers) {
        for (const auto &y : dict) salts.push_back(y-x);
    }
    for (const auto &salt : salts) {
        ll sm = 0;
        vector<bool> k(dict.size(), false);
        for (const auto &x : numbers) {
                for (ll i = 0; i < dict.size(); ++i) {
                    if (x+salt == dict[i]) k[i] = true;
                }
        }
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
