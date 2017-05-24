/**
 * Created by pippo on 2017/3/8.
 */
var gulp = require('gulp'),
    // clean = require('gulp-clean'),
    minifyCss = require('gulp-minify-css'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    clean = require('gulp-clean'),
    rev = require('gulp-rev'),
    concat = require('gulp-concat'),
    useref = require('gulp-useref'),
    revReplace = require('gulp-rev-replace'),
    revCollector = require('gulp-rev-collector'),
    fileinclude  = require('gulp-file-include'),
    runSequence = require('run-sequence');

gulp.task('clean_html',function(){
    return gulp.src('dist/html',{read:false}).pipe(clean());
});

gulp.task('clean_page',function(){
    return gulp.src('dist/pages',{read:false}).pipe(clean());
});

gulp.task('clean_js',function(){
    return gulp.src('dist/js',{read:false}).pipe(clean());
});

gulp.task('clean_css',function(){
    return gulp.src('dist/css',{read:false}).pipe(clean());
});

gulp.task('css',function(){
    return gulp.src('src/css/*.css')
    //.pipe( concat('wap.min.css') )
        .pipe(minifyCss())
        .pipe(rev())
        .pipe(gulp.dest('dist/css/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('dist/css'))
});

gulp.task('js',function(){
    return gulp.src('src/js/*.js')
        .pipe(jshint())
        .pipe(uglify())
        .pipe(rev())
        .pipe(gulp.dest('dist/js'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('dist/js'))
});

gulp.task('fileinclude', function() {
    return gulp.src('src/html/**.html')
        .pipe(fileinclude({
            prefix: '@@',
            basepath: '@file'
        }))
        .pipe(gulp.dest('dist/html'));
});

gulp.task('rev_js',function(){
    return gulp.src(['dist/js/*.json','dist/html/*.html'])
        .pipe( revCollector() )
        .pipe(gulp.dest('dist/pages'));
});

gulp.task('rev_css',function(){
    return gulp.src(['dist/css/*.json','dist/pages/*.html'])
        .pipe( revCollector() )
        .pipe(gulp.dest('dist/pages'));
});

// gulp.task('html', function () {
//     return gulp.src('dist/pages/*.html')
//         .pipe(useref())
//         .pipe(rev())
//         .pipe(revReplace())
//         .pipe(gulp.dest('dist/pages'));
// });


gulp.task('default', function(callback) {
    runSequence(
        'clean_css',
        'clean_page',
        'clean_js',
        'css',
        'js',
        'fileinclude',
        'rev_js',
        'rev_css',
        'clean_html',
        // 'html',
        callback);
});