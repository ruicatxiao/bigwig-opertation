


SOURCE="input_bw"
OUTPUT="output_bw"


for forward in $(find "$SOURCE" -name '*_FWD\.bw');
do
    FNAME=$(basename -s .bw $forward)
    reverse=$(echo $forward | sed 's/_FWD.bw/_REV.bw/')

    RNAME=$(basename -s .bw $reverse)

    echo "Now beginning the following sample: $FNAME\t$RNAME"

    # Create temporary files for processing
    tmp_fwd_bg="$FNAME.temp.bg"
    tmp_rev_bg="$RNAME.temp.bg"

    # Converting BigWig to BedGraph
    ./bigWigToBedGraph "$forward" "$tmp_fwd_bg" && echo "$FNAME forward conversion successful" || { echo "$FNAME forward conversion failed"; continue; }
    ./bigWigToBedGraph "$reverse" "$tmp_rev_bg" && echo "$RNAME reverse conversion successful" || { echo "$RNAME reverse conversion failed"; continue; }

    # Processing with awk and ensuring file is created successfully
    awk '{print $1, $2, $3, (log($4+1)/log(2))}' OFS='\t' "$tmp_fwd_bg" > "$FNAME.4COMPUTE_FWD.bg" && rm "$tmp_fwd_bg"
    awk '{print $1, $2, $3, (log($4+1)/log(2))}' OFS='\t' "$tmp_rev_bg" > "$RNAME.4COMPUTE_REV.bg" && rm "$tmp_rev_bg"

    # Converting BedGraph back to BigWig
    ./bedGraphToBigWig "$FNAME.4COMPUTE_FWD.bg" chrm.sizes "${FNAME}_4COMPUTE_FWD.bw" && rm "$FNAME.4COMPUTE_FWD.bg"
    ./bedGraphToBigWig "$RNAME.4COMPUTE_REV.bg" chrm.sizes "${RNAME}_4COMPUTE_REV.bw" && rm "$RNAME.4COMPUTE_REV.bg"



    echo "Finished sample: $FNAME\t$RNAME"
done

    mv *_4COMPUTE*.bw $OUTPUT/


