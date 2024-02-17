#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>
#include <eosiolib/transaction.hpp>
using namespace eosio;
using std::string;

// 继承eos自合约对象
class uploaddata : public eosio::contract {
private:
    // 持久化数据结构table
    /// @abi table profiles
    struct profile {
        uint64_t       key;
        string       value;
        // 主键设置为key：
        uint64_t primary_key() const { return key; }
        // 合约对象序列化：
        EOSLIB_SERIALIZE(profile, (key)(value))
    };
// 字段     类型	  说明
// key	   uint64_t	 持久化数据结构的唯一标识符,底层数据类型需要为uint64_t
// value   string	 存储的字段，类型为字符串


public:
    using contract::contract;

    // 功能：将合约账户传入合约属性_self，我们的合约账户名为uploaddata
    explicit uploaddata(account_name self) : contract(self) {} 

    /// action 1 ———— 上传 upload
    void upload(const account_name account,
		    const uint64_t key,
		    const string& value) 
    {
        // 权限验证，需要使用合约账户uploaddata
        require_auth(_self);
        
	profile_table_t profile(_self,_self);

    // 如果该文件/数据已经存储在链上了则返回报错
    // eosio_assert(uint32_t test,const char * msg)	当test的表达式结果为1时，触发msg。
	auto iter = profile.find(key);
	eosio_assert(iter == profile.end(),"Account already has profile.");

    // 链上添加该数据对。
	profile.emplace(account, [&](struct profile& p){
	    p.key = key;
	    p.value = value;
	});
        require_recipient(_self);
    
    // 上传成功
	print("profile upload");
    }


    /// action 2 ———— 查看 show ————用于数据校验
    void show(uint64_t key) 
    {
        // 无权限验证，任何使用者账户都可以查看
        profile_table_t profile(_self,_self);

        // 如果该文件/数据并不在链上则报错
        auto iter = profile.find(key);
        eosio_assert(iter != profile.end(),"Account dose not have a profile.");

    // 返回查找到的value值。
	print(iter->value.c_str());
    }


private:
    // 合约中命名table为：
    using profile_table_t = eosio::multi_index<N(profiles),profile>;
};
EOSIO_ABI(uploaddata, (upload)(show))
