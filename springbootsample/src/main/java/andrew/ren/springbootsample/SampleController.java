package andrew.ren.springbootsample;

import java.time.Duration;
import javax.annotation.PostConstruct; 

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@RestController
public class SampleController {

	@Value("${springbootsample.redis.host}")
    private String redis_host;
    
    @Value("${springbootsample.redis.port}")
    private int redis_port;
    
    Logger logger = LoggerFactory.getLogger(SampleController.class);
    
	
	@RequestMapping("/")
	public String home() {
		String output = "";
		
		try {
		    JedisPoolConfig poolConfig = new JedisPoolConfig();
		    JedisPool pool = new JedisPool(poolConfig, redis_host, redis_port);
		    Jedis jedis = pool.getResource();
		    jedis.set("test", "value");
		    if ("value" == jedis.get("test"))
		        output += "Redis Test: passed";
		    else
		        output += "Redis Test: failed";
	    }catch(Exception e){
	        output += "Redis Test: failed";
	    }
		
		
        return output;
	}
	
}