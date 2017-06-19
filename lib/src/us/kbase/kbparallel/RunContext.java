
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: RunContext</p>
 * <pre>
 * location = local | njsw
 * job_id = '' | [njsw_job_id]
 * May want to add: AWE node ID, client group, total run time, etc
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "location",
    "job_id"
})
public class RunContext {

    @JsonProperty("location")
    private String location;
    @JsonProperty("job_id")
    private String jobId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("location")
    public String getLocation() {
        return location;
    }

    @JsonProperty("location")
    public void setLocation(String location) {
        this.location = location;
    }

    public RunContext withLocation(String location) {
        this.location = location;
        return this;
    }

    @JsonProperty("job_id")
    public String getJobId() {
        return jobId;
    }

    @JsonProperty("job_id")
    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public RunContext withJobId(String jobId) {
        this.jobId = jobId;
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
        return ((((((("RunContext"+" [location=")+ location)+", jobId=")+ jobId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
