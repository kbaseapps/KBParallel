
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
 * <p>Original spec-file type: KBParallelstatusOutputObj</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "num_jobs_checked",
    "jobstatus"
})
public class KBParallelstatusOutputObj {

    @JsonProperty("num_jobs_checked")
    private Long numJobsChecked;
    @JsonProperty("jobstatus")
    private List<String> jobstatus;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("num_jobs_checked")
    public Long getNumJobsChecked() {
        return numJobsChecked;
    }

    @JsonProperty("num_jobs_checked")
    public void setNumJobsChecked(Long numJobsChecked) {
        this.numJobsChecked = numJobsChecked;
    }

    public KBParallelstatusOutputObj withNumJobsChecked(Long numJobsChecked) {
        this.numJobsChecked = numJobsChecked;
        return this;
    }

    @JsonProperty("jobstatus")
    public List<String> getJobstatus() {
        return jobstatus;
    }

    @JsonProperty("jobstatus")
    public void setJobstatus(List<String> jobstatus) {
        this.jobstatus = jobstatus;
    }

    public KBParallelstatusOutputObj withJobstatus(List<String> jobstatus) {
        this.jobstatus = jobstatus;
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
        return ((((((("KBParallelstatusOutputObj"+" [numJobsChecked=")+ numJobsChecked)+", jobstatus=")+ jobstatus)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
