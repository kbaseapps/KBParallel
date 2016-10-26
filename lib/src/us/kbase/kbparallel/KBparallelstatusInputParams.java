
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: KBparallelstatusInputParams</p>
 * <pre>
 * status() method
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "joblist"
})
public class KBparallelstatusInputParams {

    @JsonProperty("joblist")
    private List<Long> joblist;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("joblist")
    public List<Long> getJoblist() {
        return joblist;
    }

    @JsonProperty("joblist")
    public void setJoblist(List<Long> joblist) {
        this.joblist = joblist;
    }

    public KBparallelstatusInputParams withJoblist(List<Long> joblist) {
        this.joblist = joblist;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("KBparallelstatusInputParams"+" [joblist=")+ joblist)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
