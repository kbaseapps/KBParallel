
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
 * <p>Original spec-file type: KBParallelstatusInputParams</p>
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
public class KBParallelstatusInputParams {

    @JsonProperty("joblist")
    private List<String> joblist;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("joblist")
    public List<String> getJoblist() {
        return joblist;
    }

    @JsonProperty("joblist")
    public void setJoblist(List<String> joblist) {
        this.joblist = joblist;
    }

    public KBParallelstatusInputParams withJoblist(List<String> joblist) {
        this.joblist = joblist;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((("KBParallelstatusInputParams"+" [joblist=")+ joblist)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
