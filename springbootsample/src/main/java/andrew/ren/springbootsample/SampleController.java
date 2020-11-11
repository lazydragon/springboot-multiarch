package andrew.ren.springbootsample;

import java.time.Duration;
import javax.annotation.PostConstruct; 

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@RestController
public class SampleController {

	@Value("${springbootsample.redis.host}")
    private String redis_host;
    
    @Value("${springbootsample.redis.port}")
    private int redis_port;
    
    @Value("${node}")
    private String node;
    
    Logger logger = LoggerFactory.getLogger(SampleController.class);
    
	
	@RequestMapping("/")
	@ResponseBody
	public String home() {
		String output = "";
		
	    output += "Node NAME: " + node + "\n"; 
		
		output += jedisTest();
		
        return output;
	}
	
	private String jedisTest() {
		try {
		    JedisPoolConfig poolConfig = new JedisPoolConfig();
		    JedisPool pool = new JedisPool(poolConfig, redis_host, redis_port);
		    Jedis jedis = pool.getResource();
		    jedis.set("test", "value");
		    if (jedis.get("test").equals("value"))
		        return "Redis Test: passed\n";
		    else
		        return "Redis Test: failed\n";
	    }catch(Exception e){
	        return "Redis Test: failed\n";
	    }
		
	}
	
}